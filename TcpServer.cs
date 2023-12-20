using System;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;

public class TcpServer
{
    private TcpListener _server;
    private bool _isRunning;
    public bool IsRunning { get { return _isRunning; } }

    public TcpServer(string ip, int port)
    {
        _server = new TcpListener(IPAddress.Parse(ip), port);
        _isRunning = false;
    }

    public void Start()
    {
        Thread thread = new Thread(new ThreadStart(Run));
        thread.Start();
    }

    private void Run()
    {
        _server.Start();
        _isRunning = true;

        while (_isRunning)
        {
            TcpClient client = _server.AcceptTcpClient();

            byte[] data = Encoding.ASCII.GetBytes("Hello from server");
            client.GetStream().Write(data, 0, data.Length);

            

            client.Close();
        }
    }

    public void Stop()
    {
        _isRunning = false;
        _server.Stop();
    }
}