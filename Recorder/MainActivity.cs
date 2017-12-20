using Android.App;
using Android.Widget;
using Android.OS;
using System.Net.Sockets;
using System.Threading;
using Android.Media;
using System.Linq;
using System;

namespace Recorder
{
    [Activity(Label = "Recorder", MainLauncher = true, Icon = "@drawable/icon")]
    public class MainActivity : Activity
    {
        protected override void OnCreate(Bundle bundle)
        {
            base.OnCreate(bundle);

            // Set our view from the "main" layout resource
            SetContentView(Resource.Layout.Main);

            var newButton = FindViewById<Button>(Resource.Id.newRecording);
            var recordButton = FindViewById<Button>(Resource.Id.record);

            var sock = new TcpClient("192.168.1.7", 4097);
            var stream = sock.GetStream();
            var audioSource = new AudioRecord(AudioSource.Mic, 44100, ChannelIn.Mono, Encoding.Pcm16bit, 44100*5);

            newButton.Click += (_, e) => {
                stream.WriteByte(0);
            };
            recordButton.Touch += (_, e) => {
                switch(e.Event.Action) {
                    case Android.Views.MotionEventActions.Down:
                        stream.WriteByte(2);
                        var buffer = new short[4410];
                        new Thread(() => {
                            audioSource.StartRecording();
                            while(true) {
                                var count = audioSource.Read(buffer, 0, 4410);
                                if(count <= 0)
                                    break;
                                stream.WriteByte(1);
                                stream.WriteByte((byte) (count & 0xFF));
                                stream.WriteByte((byte) (count >> 8));
                                var data = buffer.Select(x => BitConverter.GetBytes(x)).SelectMany(i => i).ToArray();
                                stream.Write(data, 0, count * 2);
                            }
                            stream.WriteByte(3);
                        }).Start();
                        break;
                    case Android.Views.MotionEventActions.Up:
                        audioSource.Stop();
                        break;
                }
            };
        }
    }
}

