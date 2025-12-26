using System.Runtime.InteropServices;

namespace l8BufferCleanerApp
{
    public partial class TrayApp : Form
    {
        private NotifyIcon trayIcon;
        private const int HOTKEY_ID = 1;

        [DllImport("user32.dll")]
        private static extern bool RegisterHotKey(IntPtr hWnd, int id, int fsModifiers, int vk);

        [DllImport("user32.dll")]
        private static extern bool UnregisterHotKey(IntPtr hWnd, int id);

        const int MOD_CONTROL = 0x0002;
        const int MOD_SHIFT = 0x0004;
        const int WM_HOTKEY = 0x0312;

        public TrayApp()
        {
            //InitializeComponent();
            trayIcon = new NotifyIcon
            {
                Icon = System.Drawing.SystemIcons.Information,
                Visible = true,
                Text = "Clipboard Cleaner"
            };

            var menu = new ContextMenuStrip();
            menu.Items.Add("Очистити зараз", null, (s, e) => CleanClipboard());
            menu.Items.Add("Вихід", null, (s, e) => Exit());

            trayIcon.ContextMenuStrip = menu;

            RegisterHotKey(this.Handle, HOTKEY_ID, MOD_CONTROL | MOD_SHIFT, (int)Keys.V);
        }

        protected override void WndProc(ref Message m)
        {
            if (m.Msg == WM_HOTKEY)
            {
                CleanClipboard();
                SendKeys.SendWait("^v"); // автоматична вставка
            }
            base.WndProc(ref m);
        }

        private void CleanClipboard()
        {
            if (Clipboard.ContainsText())
            {
                string text = Clipboard.GetText(TextDataFormat.Text);
                Clipboard.Clear();
                Clipboard.SetText(text, TextDataFormat.Text);
            }
        }

        private void Exit()
        {
            UnregisterHotKey(this.Handle, HOTKEY_ID);
            trayIcon.Visible = false;
            Application.Exit();
        }

        protected override void OnFormClosing(FormClosingEventArgs e)
        {
            Exit();
            base.OnFormClosing(e);//hello
        }
    }
}

