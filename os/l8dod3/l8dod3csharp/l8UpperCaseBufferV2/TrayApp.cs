using System.Runtime.InteropServices;

namespace l8UpperCaseBufferV2
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
            trayIcon = new NotifyIcon
            {
                Icon = System.Drawing.SystemIcons.Information,
                Visible = true,
                Text = "Uppercase Paste"
            };

            var menu = new ContextMenuStrip();
            menu.Items.Add("Вставити великими літерами", null, (s, e) => UppercasePaste());
            menu.Items.Add("Вихід", null, (s, e) => Exit());

            trayIcon.ContextMenuStrip = menu;

            // Реєструємо гарячу клавішу Ctrl + Shift + V
            RegisterHotKey(this.Handle, HOTKEY_ID, MOD_CONTROL | MOD_SHIFT, (int)Keys.V);
        }

        protected override void WndProc(ref Message m)
        {
            if (m.Msg == WM_HOTKEY)
            {
                UppercasePaste();
            }
            base.WndProc(ref m);
        }

        private void UppercasePaste()
        {
            try
            {
                if (!Clipboard.ContainsText(TextDataFormat.Text))
                    return;

                string text = Clipboard.GetText(TextDataFormat.Text);
                if (string.IsNullOrEmpty(text))
                    return;

                string upper = text.ToUpperInvariant();

                SendKeys.SendWait(EscapeForSendKeys(upper));
            }
            catch
            {
                // Ігноруємо будь-які помилки, щоб не падало
            }
        }

        // Екранізація спеціальних символів для SendKeys
        private static string EscapeForSendKeys(string input)
        {
            return input
                .Replace("{", "{{}")
                .Replace("}", "{}}")
                .Replace("+", "{+}")
                .Replace("^", "{^}")
                .Replace("%", "{%}")
                .Replace("~", "{~}");
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
            base.OnFormClosing(e);
        }
    }
}
