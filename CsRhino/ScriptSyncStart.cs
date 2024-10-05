using System;

using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Reflection;
using System.Threading;

using Rhino;
using Rhino.Commands;

// using Rhino.Runtime.Code;  // FIXME: use System.Reflexion as suggested by cp

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
            // FIXME: the first  starter is throwing an error
            // start the server on a new thread
            RhinoApp.WriteLine("Starting ScriptSync for Rhino ..");
            
            // check if the IP is already in use
            try
            {
                TcpListener check = new TcpListener(IPAddress.Parse(Ip), Port);
                check.Start();
                check.Stop();
            }
            catch (Exception e)
            {
                if (e.Message.Contains("Only one usage of each socket address"))
                {
                    RhinoApp.WriteLine("Error: there are two instances of Rhino running script-sync, only one is allowed.");
                }
                else
                {
                    RhinoApp.WriteLine("Error: " + e.Message);
                }
                return Rhino.Commands.Result.Failure;
            }
            
            // if it is already in use by the instance of this Rhino
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
                scriptPath = System.IO.Path.GetFullPath(scriptPath);



                RhinoApp.InvokeOnUiThread(new Action(() =>
                {
                    try
                    {
                        // FIXME: error with C:\f:\script-sync\temp\testrh.py or C:\C:\
                        // so either is from the VSCode extension, either we need to filtering
                        // here when recived.
                        RhinoApp.WriteLine("ScriptSync reading file: " + scriptPath);

                        // string fileContent = System.IO.File.ReadAllText(scriptPath);  // TODO: this is the correct one
                        string fileContent = System.IO.File.ReadAllText("F:\\script-sync\\temp\\testrh.py");  // TODO: remove this is temproary

                        RhinoApp.WriteLine("ScriptSync running file ..");
                        
                        // the path of the assembly
                        System.IO.DirectoryInfo rhinoExePath = RhinoApp.GetExecutableDirectory();
                        string rhinoCodeAssemblyPath = System.IO.Path.Combine(rhinoExePath.FullName, "Rhino.Runtime.Code.dll");
                        Assembly rhinoCodeAssembly = Assembly.LoadFrom(rhinoCodeAssemblyPath);
                        Type scriptRunnerType = rhinoCodeAssembly.GetType("Rhino.Runtime.Code.RhinoCode");
                        if (scriptRunnerType == null)
                        {
                            RhinoApp.WriteLine("Error: RhinoCode type not found");
                            return;
                        }
                        RhinoApp.WriteLine("RhinoCode type found");  // TODO: get rid debug

                        MethodInfo runScriptMethod = scriptRunnerType.GetMethod(
                            "RunScript",
                            BindingFlags.Static | BindingFlags.Public,
                            null,
                            new Type[] { typeof(string) },
                            null
                        );
                        if (runScriptMethod == null)
                        {
                            RhinoApp.WriteLine("Error: RunScript method not found");
                            return; 
                        }
                        RhinoApp.WriteLine("RunScript method found");  // TODO: get rid debug

                        try
                        {
                            object result = runScriptMethod.Invoke(null, new object[] { fileContent });
                        }
                        catch (TargetInvocationException tie)
                        {
                            // Log the inner exception details
                            if (tie.InnerException != null)
                            {
                                RhinoApp.WriteLine("Inner Exception: " + tie.InnerException.Message);
                                RhinoApp.WriteLine("Stack Trace: " + tie.InnerException.StackTrace);
                            }
                            else
                            {
                                RhinoApp.WriteLine("Error: " + tie.Message);
                            }
                        }git
                        catch (Exception e)
                        {
                            RhinoApp.WriteLine("Error: " + e.Message);
                        }
                        
                        // RhinoCode.RunScript(fileContent);
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
            // FIXME: tests need to be revised: Error: Can not determine language for "6d7d500a-cc58-47c1-9635-3152825603f1"
            // try
            // {
            //     RhinoCode.RunScript("#! python3\nimport sys\nprint(sys.version)");
            //     RhinoCode.RunScript("#! python2\nimport sys\nprint(sys.version)");
            //     RhinoCode.RunScript("using System;\n\nCsVersion.Main();\n\nclass CsVersion\n{\n\tstatic public void Main()\n\t{\n\t\tConsole.WriteLine(\"C# Runtime: \" + Environment.Version.ToString());\n\t\tConsole.WriteLine(\"platform: \" + Environment.OSVersion.ToString());\n\t}\n}");
            // }
            // catch (Exception e)
            // {
            //     RhinoApp.WriteLine("Error from ScriptSync smoke test: " + e.Message);
            //     return false;
            // }
            return true;
        }
    }
}
