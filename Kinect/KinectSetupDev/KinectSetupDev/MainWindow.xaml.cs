using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;
using Microsoft.Kinect; //reference kinect library
using Coding4Fun.Kinect.Wpf;
using System.Collections;

namespace KinectSetupDev
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {

        /// <summary>
        /// Intermediate storage for the depth data received from the camera
        /// </summary>
        private DepthImagePixel[] depthPixels;

        /// <summary>
        /// Intermediate storage for the depth data converted to color
        /// </summary>
        private byte[] colorPixels;

        public MainWindow()
        {
            InitializeComponent();
        }

        const float MaxDepthDistance = 4096; // max value returned
        const float MinDepthDistance = 850; // min value returned
        const float MaxDepthDistanceOffset = MaxDepthDistance - MinDepthDistance;

        int rValue;
        int bValue;
        int gValue;

        private void Window_Loaded(object sender, RoutedEventArgs e)
        {
            

            kinectSensorChooser1.KinectSensorChanged += kinectSensorChooser1_KinectSensorChanged;
            bValueLbl.Content = bValue = (int)bSlider.Value;
            rValueLbl.Content = rValue = (int)rSlider.Value;
            gValueLbl.Content = gValue = (int)gSlider.Value;

        }

        void kinectSensorChooser1_KinectSensorChanged(object sender, DependencyPropertyChangedEventArgs e)//Handles what happens if we change sensors
        {
            //old sensor is stopped
            KinectSensor oldSensor = (KinectSensor)e.OldValue;
            StopKinect(oldSensor); 

            //new sensor is initialized
            KinectSensor newSensor = (KinectSensor)e.NewValue;

            if (newSensor == null)
            {
                return;
            }

            newSensor.ColorStream.Enable(ColorImageFormat.RgbResolution640x480Fps30);
            newSensor.DepthStream.Enable(DepthImageFormat.Resolution640x480Fps30);
            newSensor.SkeletonStream.Enable();

            // Allocate space to put the depth pixels we'll receive
            this.depthPixels = new DepthImagePixel[newSensor.DepthStream.FramePixelDataLength];

            // Allocate space to put the color pixels we'll create
            this.colorPixels = new byte[newSensor.DepthStream.FramePixelDataLength * sizeof(int)];

            newSensor.AllFramesReady += newSensor_AllFramesReady;
            try
            {   
                newSensor.Start();
                kinectSensorChooser1.Kinect.ElevationAngle = 0;
                currentAngleLabel.Content = tiltSelectLbl.Content = tiltSlider.Value = kinectSensorChooser1.Kinect.ElevationAngle;

            }
            catch (System.IO.IOException)
            {

                kinectSensorChooser1.AppConflictOccurred();
                
            }
        }

        private void tiltSlider_ValueChanged(object sender, RoutedPropertyChangedEventArgs<double> e)
        {
                tiltSelectLbl.Content = (int)tiltSlider.Value;
            
        }
        
        private void bSlider_ValueChanged(object sender, RoutedPropertyChangedEventArgs<double> e)
        {
            if (kinectSensorChooser1.Kinect != null && kinectSensorChooser1.Kinect.IsRunning)
            {
                bValueLbl.Content = bValue = (int)bSlider.Value;
            }
        }

        private void gSlider_ValueChanged(object sender, RoutedPropertyChangedEventArgs<double> e)
        {
            if (kinectSensorChooser1.Kinect != null && kinectSensorChooser1.Kinect.IsRunning)
            {
                gValueLbl.Content = gValue = (int)gSlider.Value;
            }
        }

        private void rSlider_ValueChanged(object sender, RoutedPropertyChangedEventArgs<double> e)
        {
            if (kinectSensorChooser1.Kinect != null && kinectSensorChooser1.Kinect.IsRunning)
            {
                rValueLbl.Content = rValue = (int)rSlider.Value;
            }
        }
 
        private void button1_Click(object sender, RoutedEventArgs e)
        {
            button1.IsEnabled = false;

            //set angle to slider value
            if (kinectSensorChooser1.Kinect != null && kinectSensorChooser1.Kinect.IsRunning)
            {
                currentAngleLabel.Content = kinectSensorChooser1.Kinect.ElevationAngle = (int)tiltSlider.Value;
                
            }

            button1.IsEnabled = true;

        }

        //Trying to create monochrome background for all other pixels from red. Unsure if getting depth data as intensity is at 255
        void newSensor_AllFramesReady(object sender, AllFramesReadyEventArgs e)
        {
            int minDepth;
               int maxDepth;
            ArrayList isolatedDepthPixels = new ArrayList();
            //get the raw data from kinect with the depth for every pixel
            using (DepthImageFrame depthFrame = e.OpenDepthImageFrame())
            {
                if (depthFrame == null)
                {
                    return;
                }

                depthFrame.CopyDepthImagePixelDataTo(this.depthPixels);

                // Get the min and max reliable depth for the current frame
                minDepth = depthFrame.MinDepth;
                maxDepth = depthFrame.MaxDepth;
              
                

            }

            using (ColorImageFrame colorFrame = e.OpenColorImageFrame())
            {
                if (colorFrame == null)
                {
                    return;
                }

                
                colorFrame.CopyPixelDataTo(colorPixels);

                const int GreenIndex = 1;
                const int RedIndex = 2;
                const int BlueIndex = 0;

                

                for (int colorIndex = 0, depthIndex = 0; depthIndex < this.depthPixels.Length && colorIndex < colorPixels.Length; colorIndex += 4)
                {
                    short depth = depthPixels[depthIndex].Depth;
                    
                    if (colorPixels[colorIndex + RedIndex] >= rValue && colorPixels[colorIndex + BlueIndex] <= bValue && colorPixels[colorIndex + GreenIndex] <= gValue)
                    {
                        colorPixels[colorIndex + BlueIndex] = 0;
                        colorPixels[colorIndex + GreenIndex] = 255;
                        colorPixels[colorIndex + RedIndex] = 0;

                        isolatedDepthPixels.Add(depth);
                    }
                    
                    /*
                         byte intensity = (byte)(depth >= minDepth && depth <= maxDepth ? depth : 0);
                         this.colorPixels[colorIndex + BlueIndex] = intensity;
                         this.colorPixels[colorIndex + GreenIndex] = intensity;
                         this.colorPixels[colorIndex + RedIndex] = intensity;
                     * */
                     


                }
                int avg = 0;
                foreach (short obj in isolatedDepthPixels)
                {
                    avg = avg + obj;
                }
                avg = avg / isolatedDepthPixels.Count;

                avgDist.Content = avg;

                int stride = colorFrame.Width * 4;
                depthImage.Source =
                    BitmapSource.Create(colorFrame.Width, colorFrame.Height,
                    96, 96, PixelFormats.Bgr32, null, colorPixels, stride);
            }
        }

        private byte[] GenerateColoredBytes(DepthImageFrame depthFrame)
        {   
            //get raw data from kinect with the depth for every pixel
            short[] rawDepthData = new short[depthFrame.PixelDataLength];
            depthFrame.CopyPixelDataTo(rawDepthData);

            //use depthFrame to create the imag eto display on screen
            //depthFrame contains color information for all pixels in image
            //Height x Width x 4 (Blue,Green,Red, empty byte)
            Byte[] pixels = new byte[depthFrame.Height * depthFrame.Width * 4];

            //Bgr32 - Blue, gren, red, empty byte
            //Bgra32 - Blue, green, red, transparency
            //You mist set transparency for Bgra as .NET defaults a byte to 0 = full transparency

            //hardcoded location to Blue, Green, Red )BGR) index positions
            const int BlueIndex = 0;
            const int GreenIndex = 1;
            const int RedIndex = 2;

            //loop through all distances
            //pick RGB color based on distance
            for (int depthIndex = 0, colorIndex = 0; depthIndex < rawDepthData.Length && colorIndex < pixels.Length; depthIndex++, colorIndex += 4)
            {
                //get the player (requires skeleton tracking enabled for values)
                int player = rawDepthData[depthIndex] & DepthImageFrame.PlayerIndexBitmask;

                //gets the depth value
                int depth = rawDepthData[depthIndex] >> DepthImageFrame.PlayerIndexBitmaskWidth;

                //if 0.9 meters
                if (depth <= 900)
                {
                    //we are very close
                    pixels[colorIndex + BlueIndex] = 255;
                    pixels[colorIndex + GreenIndex] = 0;
                    pixels[colorIndex + GreenIndex] = 0;
                }
                
                //else if between 0.9 meters and 2 meters
                else if (depth > 900 && depth < 2000)
                {
                    pixels[colorIndex + BlueIndex] = 0;
                    pixels[colorIndex + GreenIndex] = 255;
                    pixels[colorIndex + GreenIndex] = 0;
                }

                else
                {
                    pixels[colorIndex + BlueIndex] = 0;
                    pixels[colorIndex + GreenIndex] = 0;
                    pixels[colorIndex + GreenIndex] = 255;
                }

                ////equal coloring for monochromatic histogram
                byte intensity = CalculateIntensityFromDepth(depth);
                pixels[colorIndex + BlueIndex] = intensity;
                pixels[colorIndex + GreenIndex] = intensity;
                pixels[colorIndex + RedIndex] = intensity;


                //Color all players "gold"
                if (player > 0)
                {
                    pixels[colorIndex + BlueIndex] = Colors.Gold.B;
                    pixels[colorIndex + GreenIndex] = Colors.Gold.G;
                    pixels[colorIndex + RedIndex] = Colors.Gold.R;
                }

            }

            return pixels;

        }

        public static byte CalculateIntensityFromDepth(int distance)
        {
            //formula for calculating monochrome intensity for histogram
            return (byte)(255 - (255 * Math.Max(distance - MinDepthDistance, 0)
                / (MaxDepthDistanceOffset)));
        }

        void StopKinect(KinectSensor sensor)
        {
            if (sensor != null)
            {
                if (sensor.IsRunning)
                {
                    kinectSensorChooser1.Kinect.ElevationAngle = 0;
                    sensor.Stop();
                    if (sensor.AudioSource != null)
                    {
                        sensor.AudioSource.Stop();
                    }
                }
            }
        }

        void Window_Closing(object sender, System.ComponentModel.CancelEventArgs e)
        {   
            //stops the currently "kinected" sensor (And you thought I was finsished!!!)
            StopKinect(kinectSensorChooser1.Kinect);
        }

        

        

        

        
        
    }
    
}
