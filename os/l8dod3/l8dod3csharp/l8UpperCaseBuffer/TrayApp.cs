using System.Runtime.InteropServices;

namespace l8UpperCaseBuffer
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
                Text = "Uppercase Clipboard"
            };

            var menu = new ContextMenuStrip();
            menu.Items.Add("Uppercase now", null, (s, e) => UppercaseClipboard());
            menu.Items.Add("Exit", null, (s, e) => Exit());

            trayIcon.ContextMenuStrip = menu;

            RegisterHotKey(this.Handle, HOTKEY_ID, MOD_CONTROL | MOD_SHIFT, (int)Keys.V);
        }

        protected override void WndProc(ref Message m)
        {
            if (m.Msg == WM_HOTKEY)
            {
                UppercaseClipboard();
                SendKeys.SendWait("^v");
            }
            base.WndProc(ref m);
        }

        private void UppercaseClipboard()
        {
            if (!Clipboard.ContainsText())
                return;
            string text = Clipboard.GetText(); // БЕЗ очищення форматування
            var upperText = text?.ToUpper();
            if (string.IsNullOrEmpty(text))
            {
                return;
            }
            Clipboard.SetText(upperText);
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
/*
 * 
 * 
 * 
 * Studio Code.org

Code.org
https://studio.code.org
Flappy Code. Wanna write your own game in less than 10 minutes? Try our Flappy Code tutorial!Read more
 */