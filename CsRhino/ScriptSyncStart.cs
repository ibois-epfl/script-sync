using System;
using System.Collections.Generic;

using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;

using Rhino;
using Rhino.Commands;
using Rhino.Geometry;
using Rhino.Input;
using Rhino.Input.Custom;


namespace ScriptSync
{
    [Rhino.Commands.CommandStyle(Rhino.Commands.Style.ScriptRunner)]
    public class ScriptSyncStart : Command
    {
        /// <summary> The server that listens for incoming paths to run. </summary>
        private TcpListener _server;
        /// <summary> The thread that runs the server. </summary>
        public Thread WorkerThread { get; set; }
        /// <summary> Whether the server is running or not. </summary>
        public bool IsRunning { get; set; }
        /// <summary> The IP address of the server. </summary>
        public string Ip = "127.0.0.1";
        /// <summary> The port of the server. </summary>
        public int Port = 58259;

        public ScriptSyncStart()
        {
            Instance = this;
        }

        public static ScriptSyncStart Instance { get; private set; }

        public override string EnglishName => "ScriptSyncStart";

        protected override Rhino.Commands.Result RunCommand(RhinoDoc doc, RunMode mode)
        {
            // initialize the ScriptEditor if it is not already
            RhinoApp.RunScript("_-ScriptEditor _Enter", false);

            // start the server on a new thread
            RhinoApp.WriteLine("Starting ScriptSync..");
            if (IsRunning)
            {
                RhinoApp.WriteLine("Server already running");
                return Rhino.Commands.Result.Success;
            }
            _server = new TcpListener(IPAddress.Parse(Ip), Port);
            IsRunning = false;

            Thread WorkerThread = new Thread(new ThreadStart(Run));
            WorkerThread.Start();

            return Rhino.Commands.Result.Success;
        }

        /// <summary>
        /// It is called on a thread to run the server and listen for incoming paths to run.
        /// </summary>
        public void Run()
        {
            _server.Start();
            IsRunning = true;

            RhinoApp.InvokeOnUiThread(new Action(() =>
            {
                if (!IsScriptEditorRunnerFromThreadOk())
                    RhinoApp.WriteLine("Warning: ScriptEditorRunner is failing starting tests");
            }));

            while (IsRunning)
            {
                TcpClient client = _server.AcceptTcpClient();
                byte[] data = new byte[1024];
                NetworkStream stream = client.GetStream();
                int bytesRead = stream.Read(data, 0, data.Length);
                string scriptPath = Encoding.ASCII.GetString(data, 0, bytesRead);

                if (bytesRead == 0)
                {
                    IsRunning = false;
                    break;
                }

                RhinoApp.InvokeOnUiThread(new Action(() =>
                {
                    try
                    {
                        RhinoApp.RunScript("_-ScriptEditor Run " + scriptPath, true);
                    }
                    catch (Exception e)
                    {
                        RhinoApp.WriteLine("Error: " + e.Message);
                    }
                }));
            }
            _server.Stop();
            RhinoApp.InvokeOnUiThread(new Action(() =>
            {
                RhinoApp.WriteLine("ScriptSync stopped");
            }));
        }

        /// <summary>
        /// The ScriptEditor on a thread needs a dry run to be able to run scripts.
        /// </summary>
        /// <returns> true if the dry run is ok </returns>
        private bool IsScriptEditorRunnerFromThreadOk()
        {
            string cPyScriptPath = System.IO.Path.GetFullPath(@"./temp/cpy_version.py");
            string ironPyScriptPath = System.IO.Path.GetFullPath(@"./temp/ironpy_version.py");
            string csScriptPath = System.IO.Path.GetFullPath(@"./temp/CsVersion.cs");

            System.IO.File.WriteAllText(cPyScriptPath, "#! python3\nimport sys\nprint(sys.version)");
            System.IO.File.WriteAllText(ironPyScriptPath, "#! python2\nimport sys\nprint(sys.version)");
            System.IO.File.WriteAllText(csScriptPath, "using System;\n\nCsVersion.Main();\n\nclass CsVersion\n{\n\tstatic public void Main()\n\t{\n\t\tConsole.WriteLine(\"C# Runtime: \" + Environment.Version.ToString());\n\t\tConsole.WriteLine(\"platform: \" + Environment.OSVersion.ToString());\n\t}\n}");

            bool cPyIsRunning = RhinoApp.RunScript("_-ScriptEditor Run " + cPyScriptPath, true);
            bool ironPyIsRunning = RhinoApp.RunScript("_-ScriptEditor Run " + ironPyScriptPath, true);
            bool csIsRunning = RhinoApp.RunScript("_-ScriptEditor Run " + csScriptPath, true);

            System.IO.File.Delete(cPyScriptPath);
            System.IO.File.Delete(ironPyScriptPath);
            System.IO.File.Delete(csScriptPath);

            if (!cPyIsRunning || !ironPyIsRunning || !csIsRunning)
                return false;
            return true;
        }
    }
}
