"""
Main GUI application using ttkbootstrap.
"""

import threading
from datetime import datetime
from pathlib import Path
from tkinter import filedialog
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox

# Add parent directory to path for imports
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from api.etherscan import EtherscanClient, EtherscanAPIError
from export.xlsx_handler import XlsxHandler
from utils.helpers import (
    validate_eth_address,
    get_date_range_blocks
)
from utils.config import Config


class WalletExporterApp:
    """Main application window for the ERC-20 Transaction Exporter."""

    def __init__(self):
        """Initialize the application."""
        self.root = ttk.Window(
            title="ERC-20 Transaction Exporter",
            themename="cosmo",
            size=(750, 700),
            resizable=(True, True)
        )
        self.root.minsize(650, 600)

        # Config for saving settings
        self.config = Config()

        # Variables
        self.api_key_var = ttk.StringVar()
        self.is_exporting = False

        # Batch wallet list: [(address, file_path, selected_var), ...]
        self.batch_wallets = []

        # Load saved API key
        saved_key = self.config.get_api_key()
        if saved_key:
            self.api_key_var.set(saved_key)

        self._create_widgets()
        self._load_saved_wallets()

    def _create_widgets(self):
        """Create all GUI widgets."""
        # Main container with padding
        main_frame = ttk.Frame(self.root, padding=15)
        main_frame.pack(fill=BOTH, expand=YES)

        # API Key Section
        self._create_api_section(main_frame)

        # Add wallet section
        self._create_add_wallet_section(main_frame)

        # Wallet list section
        self._create_wallet_list_section(main_frame)

        # Date Range section
        self._create_date_section(main_frame)

        # Progress & Export
        self._create_export_section(main_frame)

    def _create_api_section(self, parent):
        """Create the API key input section."""
        frame = ttk.LabelFrame(parent, text="Etherscan API Key")
        frame.pack(fill=X, pady=(0, 10))

        inner = ttk.Frame(frame, padding=10)
        inner.pack(fill=X)

        ttk.Entry(
            inner,
            textvariable=self.api_key_var,
            width=50,
            show="*"
        ).pack(side=LEFT, fill=X, expand=YES, padx=(0, 10))

        ttk.Button(
            inner,
            text="Save",
            command=self._save_api_key,
            bootstyle="success-outline",
            width=8
        ).pack(side=LEFT, padx=(0, 5))

        ttk.Button(
            inner,
            text="Test",
            command=self._test_api_connection,
            bootstyle="info-outline",
            width=8
        ).pack(side=LEFT)

    def _save_api_key(self):
        """Save the API key to config."""
        api_key = self.api_key_var.get().strip()
        if api_key:
            self.config.save_api_key(api_key)
            Messagebox.show_info("API key saved!", "Saved")
        else:
            Messagebox.show_warning("Please enter an API key first.", "No Key")

    def _create_add_wallet_section(self, parent):
        """Create the add wallet section."""
        frame = ttk.LabelFrame(parent, text="Add Wallet")
        frame.pack(fill=X, pady=(0, 10))

        inner = ttk.Frame(frame, padding=10)
        inner.pack(fill=X)

        # Wallet address input
        addr_frame = ttk.Frame(inner)
        addr_frame.pack(fill=X, pady=(0, 5))

        ttk.Label(addr_frame, text="Wallet:", width=8).pack(side=LEFT)
        self.batch_addr_var = ttk.StringVar()
        ttk.Entry(
            addr_frame,
            textvariable=self.batch_addr_var,
            width=55
        ).pack(side=LEFT, fill=X, expand=YES)

        # File path input
        file_frame = ttk.Frame(inner)
        file_frame.pack(fill=X, pady=(0, 5))

        ttk.Label(file_frame, text="File:", width=8).pack(side=LEFT)
        self.batch_file_var = ttk.StringVar()
        ttk.Entry(
            file_frame,
            textvariable=self.batch_file_var,
            width=40
        ).pack(side=LEFT, fill=X, expand=YES, padx=(0, 10))

        ttk.Button(
            file_frame,
            text="Select",
            command=self._select_batch_wallet_file,
            bootstyle="info-outline",
            width=8
        ).pack(side=LEFT, padx=(0, 5))

        ttk.Button(
            file_frame,
            text="New",
            command=self._create_batch_wallet_file,
            bootstyle="primary-outline",
            width=8
        ).pack(side=LEFT)

        # Add button
        ttk.Button(
            inner,
            text="Add to List",
            command=self._add_batch_wallet,
            bootstyle="success",
            width=15
        ).pack(pady=(5, 0))

    def _create_wallet_list_section(self, parent):
        """Create the wallet list section with checkboxes."""
        frame = ttk.LabelFrame(parent, text="Wallet List")
        frame.pack(fill=BOTH, expand=YES, pady=(0, 10))

        # Button row for select/deselect
        btn_frame = ttk.Frame(frame, padding=(10, 10, 10, 0))
        btn_frame.pack(fill=X)

        ttk.Button(
            btn_frame,
            text="Select All",
            command=self._select_all_wallets,
            bootstyle="info-outline",
            width=12
        ).pack(side=LEFT, padx=(0, 5))

        ttk.Button(
            btn_frame,
            text="Deselect All",
            command=self._deselect_all_wallets,
            bootstyle="secondary-outline",
            width=12
        ).pack(side=LEFT, padx=(0, 5))

        ttk.Button(
            btn_frame,
            text="Remove Selected",
            command=self._remove_selected_wallets,
            bootstyle="danger-outline",
            width=15
        ).pack(side=RIGHT)

        # Scrollable frame for wallet list
        list_container = ttk.Frame(frame, padding=10)
        list_container.pack(fill=BOTH, expand=YES)

        # Canvas and scrollbar for scrolling
        self.canvas = ttk.Canvas(list_container, height=150)
        scrollbar = ttk.Scrollbar(list_container, orient=VERTICAL, command=self.canvas.yview)

        self.wallet_list_frame = ttk.Frame(self.canvas)

        self.canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side=RIGHT, fill=Y)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=YES)

        self.canvas_window = self.canvas.create_window((0, 0), window=self.wallet_list_frame, anchor=NW)

        self.wallet_list_frame.bind("<Configure>", self._on_frame_configure)
        self.canvas.bind("<Configure>", self._on_canvas_configure)

    def _on_frame_configure(self, event):
        """Reset the scroll region to encompass the inner frame."""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_canvas_configure(self, event):
        """Resize the inner frame to match canvas width."""
        self.canvas.itemconfig(self.canvas_window, width=event.width)

    def _load_saved_wallets(self):
        """Load saved wallet list from config."""
        saved_wallets = self.config.get_wallet_list()
        for wallet in saved_wallets:
            address = wallet.get("address", "")
            file_path = wallet.get("file_path", "")
            if address and file_path:
                selected_var = ttk.BooleanVar(value=True)
                self.batch_wallets.append((address, file_path, selected_var))
                self._add_wallet_row(address, file_path, selected_var)

    def _save_wallet_list(self):
        """Save current wallet list to config."""
        wallets = [
            {"address": addr, "file_path": path}
            for addr, path, _ in self.batch_wallets
        ]
        self.config.save_wallet_list(wallets)

    def _select_batch_wallet_file(self):
        """Select existing file for batch wallet."""
        file_path = filedialog.askopenfilename(
            title="Select Existing Excel File",
            filetypes=[("Excel files", "*.xlsx")],
            defaultextension=".xlsx",
            initialdir=self.config.get_last_directory()
        )
        if file_path:
            self.batch_file_var.set(file_path)
            self.config.save_last_directory(str(Path(file_path).parent))

    def _create_batch_wallet_file(self):
        """Create new file for batch wallet."""
        file_path = filedialog.asksaveasfilename(
            title="Create New Excel File",
            filetypes=[("Excel files", "*.xlsx")],
            defaultextension=".xlsx",
            initialdir=self.config.get_last_directory()
        )
        if file_path:
            self.batch_file_var.set(file_path)
            self.config.save_last_directory(str(Path(file_path).parent))

    def _add_batch_wallet(self):
        """Add a wallet to the batch list."""
        address = self.batch_addr_var.get().strip()
        file_path = self.batch_file_var.get().strip()

        if not validate_eth_address(address):
            Messagebox.show_warning(
                "Please enter a valid Ethereum address.",
                "Invalid Address"
            )
            return

        if not file_path:
            Messagebox.show_warning(
                "Please select or create an export file.",
                "Missing File"
            )
            return

        # Create checkbox variable
        selected_var = ttk.BooleanVar(value=True)

        # Add to list
        self.batch_wallets.append((address, file_path, selected_var))

        # Create row in UI
        self._add_wallet_row(address, file_path, selected_var)

        # Save to config
        self._save_wallet_list()

        # Clear inputs
        self.batch_addr_var.set("")
        self.batch_file_var.set("")

    def _add_wallet_row(self, address: str, file_path: str, selected_var):
        """Add a wallet row to the list UI."""
        row_frame = ttk.Frame(self.wallet_list_frame)
        row_frame.pack(fill=X, pady=2)

        ttk.Checkbutton(
            row_frame,
            variable=selected_var,
            bootstyle="success-round-toggle"
        ).pack(side=LEFT, padx=(0, 10))

        ttk.Label(
            row_frame,
            text=f"{address[:20]}...",
            width=25
        ).pack(side=LEFT)

        ttk.Label(
            row_frame,
            text=Path(file_path).name,
            width=30
        ).pack(side=LEFT, padx=(10, 0))

    def _refresh_wallet_list(self):
        """Refresh the wallet list UI."""
        # Clear existing widgets
        for widget in self.wallet_list_frame.winfo_children():
            widget.destroy()

        # Recreate rows
        for address, file_path, selected_var in self.batch_wallets:
            self._add_wallet_row(address, file_path, selected_var)

    def _select_all_wallets(self):
        """Select all wallets."""
        for _, _, selected_var in self.batch_wallets:
            selected_var.set(True)

    def _deselect_all_wallets(self):
        """Deselect all wallets."""
        for _, _, selected_var in self.batch_wallets:
            selected_var.set(False)

    def _remove_selected_wallets(self):
        """Remove wallets that are checked."""
        self.batch_wallets = [
            (addr, path, var) for addr, path, var in self.batch_wallets
            if not var.get()
        ]
        self._refresh_wallet_list()
        self._save_wallet_list()

    def _create_date_section(self, parent):
        """Create date range picker section."""
        frame = ttk.LabelFrame(parent, text="Date Range (Optional - leave empty for all transactions)")
        frame.pack(fill=X, pady=(0, 10))

        inner = ttk.Frame(frame, padding=10)
        inner.pack(fill=X)

        # From date
        from_frame = ttk.Frame(inner)
        from_frame.pack(side=LEFT, padx=(0, 20))

        ttk.Label(from_frame, text="From:").pack(side=LEFT, padx=(0, 5))
        self.from_date = ttk.DateEntry(
            from_frame,
            bootstyle="primary",
            dateformat="%d/%m/%Y"
        )
        self.from_date.pack(side=LEFT)

        # To date
        to_frame = ttk.Frame(inner)
        to_frame.pack(side=LEFT)

        ttk.Label(to_frame, text="To:").pack(side=LEFT, padx=(0, 5))
        self.to_date = ttk.DateEntry(
            to_frame,
            bootstyle="primary",
            dateformat="%d/%m/%Y"
        )
        self.to_date.pack(side=LEFT)

        # Clear dates button
        ttk.Button(
            inner,
            text="Clear",
            command=self._clear_dates,
            bootstyle="secondary-outline",
            width=8
        ).pack(side=RIGHT)

    def _clear_dates(self):
        """Clear the date entries."""
        self.from_date.entry.delete(0, 'end')
        self.to_date.entry.delete(0, 'end')

    def _create_export_section(self, parent):
        """Create progress bar and export button."""
        # Progress
        self.progress_bar = ttk.Progressbar(
            parent,
            mode="determinate",
            bootstyle="success-striped"
        )
        self.progress_bar.pack(fill=X, pady=(0, 10))

        # Export Button
        self.export_btn = ttk.Button(
            parent,
            text="Export Selected Wallets",
            command=self._start_export,
            bootstyle="success",
            width=25
        )
        self.export_btn.pack()

    def _test_api_connection(self):
        """Test the API key connection."""
        api_key = self.api_key_var.get().strip()
        if not api_key:
            Messagebox.show_warning("Please enter an API key.", "Missing API Key")
            return

        client = EtherscanClient(api_key)
        if client.test_connection():
            Messagebox.show_info("API connection successful!", "Success")
        else:
            Messagebox.show_error("Invalid API key or connection failed.", "Error")

    def _get_date_range(self) -> tuple[int | None, int | None]:
        """Get Unix timestamps from date entries."""
        try:
            from_date = self.from_date.entry.get()
            to_date = self.to_date.entry.get()

            start_ts = None
            end_ts = None

            if from_date:
                from_dt = datetime.strptime(from_date, "%d/%m/%Y")
                start_ts, _ = get_date_range_blocks(from_dt, from_dt)

            if to_date:
                to_dt = datetime.strptime(to_date, "%d/%m/%Y")
                _, end_ts = get_date_range_blocks(to_dt, to_dt)

            return start_ts, end_ts
        except ValueError:
            return None, None

    def _start_export(self):
        """Start the export process."""
        if self.is_exporting:
            return

        # Validate inputs
        api_key = self.api_key_var.get().strip()
        if not api_key:
            Messagebox.show_warning("Please enter your Etherscan API key.", "Missing API Key")
            return

        # Get selected wallets
        selected_wallets = [
            (addr, path) for addr, path, var in self.batch_wallets
            if var.get()
        ]

        if not selected_wallets:
            Messagebox.show_warning(
                "No wallets selected. Check the wallets you want to export.",
                "No Selection"
            )
            return

        self.is_exporting = True
        self.export_btn.configure(state="disabled")
        self.progress_bar["maximum"] = len(selected_wallets)
        self.progress_bar["value"] = 0

        # Run export in separate thread
        thread = threading.Thread(
            target=self._run_export,
            args=(selected_wallets,),
            daemon=True
        )
        thread.start()

    def _run_export(self, wallets: list):
        """Execute the export (runs in thread)."""
        try:
            api_key = self.api_key_var.get().strip()
            start_ts, end_ts = self._get_date_range()

            client = EtherscanClient(api_key)
            total_added = 0
            results = []

            for i, (address, file_path) in enumerate(wallets, 1):
                self.root.after(0, lambda v=i: self.progress_bar.configure(value=v))

                try:
                    transactions = client.get_erc20_transactions(
                        address,
                        start_timestamp=start_ts,
                        end_timestamp=end_ts
                    )
                    handler = XlsxHandler(file_path)
                    added = handler.append_transactions(transactions)
                    total_added += added
                    results.append(f"{address[:10]}...: {added} tx")
                except EtherscanAPIError as e:
                    results.append(f"{address[:10]}...: Error")

            result_text = "\n".join(results)
            self.root.after(0, lambda: Messagebox.show_info(
                f"Processed {len(wallets)} wallets\nTotal: {total_added} transactions\n\n{result_text}",
                "Export Complete"
            ))

        except Exception as e:
            self.root.after(0, lambda: Messagebox.show_error(str(e), "Error"))

        finally:
            self.is_exporting = False
            self.root.after(0, self._reset_ui)

    def _reset_ui(self):
        """Reset UI after export."""
        self.export_btn.configure(state="normal")
        self.progress_bar["value"] = 0

    def run(self):
        """Start the application."""
        self.root.mainloop()
