using System;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Linq;

namespace SimpleIO {
    public partial class DefaultForm : Form {
        public DefaultForm() {
            InitializeComponent();
        }

        private void button1_Click(object sender, EventArgs e) {
            Close();
        }

        struct ManagerOutput {
            public bool success;
            public string[] lines;
        }

        private void button2_Click(object sender, EventArgs e) {
            string[] tbtext = tbInput.Lines;
            button2.Enabled = false;
            button2.Text = "Ждите результат...";
            tbOutput.Text = "";

            var serv = new MicroServerAPI.MicroService("http://localhost:8080/5-semestr/compiler/get-job", "http://localhost:8080/5-semestr/compiler/post-job");

            ManagerOutput result = new ManagerOutput();

            Task.Run(() => {
                result = serv.ProcessAsFunction<ManagerOutput, string[]>("Compilation.Manager.Input.Pascal", 
                    tbtext,
                    "Compilation.Manager.Output");

            }).ContinueWith((task) => {
                if (task.IsCompletedSuccessfully) {
                    if (result.success) {
                        tbOutput.Lines = result.lines;
                    } else {
                        tbOutput.Lines = result.lines.Prepend("[!] Ошибка:").ToArray();
                    }
                } else {
                    MessageBox.Show("Произошла ошибка: " + task.Exception.Message + "\nУчтите, persistentMode (persistentConnections) неактивен: возможно, система ещё запускается, подождите и попробуйте снова позже.", "Ошибка подключения к серверу", MessageBoxButtons.OK, MessageBoxIcon.Error);
                }
                button2.Enabled = true;
                button2.Text = "Скомпилировать";
            }, TaskScheduler.FromCurrentSynchronizationContext());
        }

        private void DefaultForm_FormClosing(object sender, FormClosingEventArgs e) {
            if (!button2.Enabled) {
                var result = MessageBox.Show("А вот этого делать не рекомендуется во время ожидания результата!\nЕсли вы выйдете сейчас, результат текущих вычислений будет занимать место на сервере, но получить его данная программа не сможет!\nВы согласны ещё подождать?", "Предупреждение", MessageBoxButtons.YesNo, MessageBoxIcon.Warning, MessageBoxDefaultButton.Button1);
                if (result == DialogResult.Yes)
                    e.Cancel = true;
            }
        }

        private void timer1_Tick(object sender, EventArgs e) {
            if (ActiveForm != this) {
               Activate();
            }
        }

        private void tbInput_DragEnter(object sender, DragEventArgs e) {
            if (e.Data.GetDataPresent(typeof(string))) {
                e.Effect = DragDropEffects.Copy;
            }
        }

        private void tbInput_DragDrop(object sender, DragEventArgs e) {
            if (e.Effect == DragDropEffects.Copy) {
                object item = e.Data.GetData(typeof(string));
                tbInput.Text = (string)item;
            }
        }
    }
}
