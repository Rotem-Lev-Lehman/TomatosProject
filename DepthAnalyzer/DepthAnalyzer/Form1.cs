using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Drawing.Drawing2D;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace DepthAnalyzer
{
    public partial class frmDepthAnalyzer : Form
    {


        public frmDepthAnalyzer()
        {
            InitializeComponent();

            //this.MouseWheel += new MouseEventHandler(OnMouseWheel);
        }
        Bitmap bmp = null;
        int[,] depth = null;


        private bool GetFileNames(out string sRGBFileName, out string sDepthFileName)
        {
            OpenFileDialog dlg = new OpenFileDialog();
            dlg.Multiselect = true;
            dlg.Title = "Choose an RGB and a depth image";
            sRGBFileName = "";
            sDepthFileName = "";
            if (dlg.ShowDialog() == DialogResult.OK)
            {
                while (dlg.FileNames.Count() != 2)
                {
                    MessageBox.Show("You must select exactly 2 files - RGB and depth");
                    if (dlg.ShowDialog() == DialogResult.Cancel)
                        return false;
                }

                sRGBFileName = dlg.FileNames[0];
                sDepthFileName = dlg.FileNames[1];
                if (sRGBFileName.ToLower().Contains("depth"))
                {
                    string sAux = sRGBFileName;
                    sRGBFileName = sDepthFileName;
                    sDepthFileName = sAux;
                }


                return true;
            }
            return false;
        }

        private bool GetFileNames2(out string sRGBFileName, out string sDepthFileName)
        {
            OpenFileDialog dlg = new OpenFileDialog();
            sRGBFileName = "";
            sDepthFileName = "";
            if (dlg.ShowDialog() == DialogResult.OK)
            {
                sRGBFileName = dlg.FileName;
                //picRGB.Image = bmp;
                SetImage(picRGB, bmp);
                SetImage(picOrg, bmp);

                



                string sFolder = dlg.FileName.Substring(0, dlg.FileName.LastIndexOf('\\') + 1);
                string sFileName = dlg.FileName.Substring(dlg.FileName.LastIndexOf('\\') + 1);
                //20190813_094528_color_3.png
                //20190813_094528_depth_3.tiff
                string sIdx = sFileName.Substring(sFileName.IndexOf('_') + 1);
                string sDepth = sIdx.Replace("color", "depth").Replace("png", "tiff");
                DirectoryInfo dir = new DirectoryInfo(sFolder);
                foreach (FileInfo f in dir.GetFiles())
                {
                    if (f.Name.Contains(sDepth))
                        sDepthFileName = f.FullName;
                }

                return true;
            }
            return false;
        }

        private void BtnLoad_Click(object sender, EventArgs e)
        {
            string sRGB, sDepth;

            if (!GetFileNames(out sRGB, out sDepth))
                return;

            m_dZoomscale = 1.0f;

            bmp = new Bitmap(sRGB);

            SetImage(picRGB, bmp);
            SetImage(picOrg, bmp);

            BitmapEx bmpexDepth = new BitmapEx(sDepth);

            //Bitmap bmpDepth = new Bitmap(sDepthFileName);
            depth = new int[bmp.Width, bmp.Height];
            int iMin = 10000, iMax = 0;
            /*
            for (int i = 0; i < bmp.Width; i++)
            {
                for (int j = 0; j < bmp.Height; j++)
                {
                    Color c = bmpexDepth.GetPixel(i, j);
                    //Color c = bmpDepth.GetPixel(i, j);
                    //if (bmpDepth.GetPixel(i, j).R > 3)
                    //    Console.Write("*");
                    //depth[i, j] = bmpDepth.GetPixel(i, j).R + bmpDepth.GetPixel(i, j).G + bmpDepth.GetPixel(i, j).B;
                    depth[i, j] = bmpexDepth.GetPixel(i, j).R + bmpexDepth.GetPixel(i, j).G + bmpexDepth.GetPixel(i, j).B;
                    if (depth[i, j] < iMin)
                        iMin = depth[i, j];
                    if (depth[i, j] > iMax)
                        iMax = depth[i, j];
                }
            }
            */

            SortedDictionary<int, int> dDepths = new SortedDictionary<int, int>();

            try
            {
                bmpexDepth.LockBits();
                unsafe
                {
                    int index, x, y;
                    int stride = bmp.Width * bmpexDepth.ChannelCount;
                    ushort* pix = (ushort*)bmpexDepth.Scan0;
                    for (y = 0; y < bmp.Height; y++)
                    {
                        for (x = 0; x < bmp.Width; x++)
                        {
                            index = y * stride + (x * bmpexDepth.ChannelCount);

                            int iCentimeter = pix[index] / 10;
                            if (!dDepths.ContainsKey(iCentimeter))
                                dDepths[iCentimeter] = 0;
                            dDepths[iCentimeter]++;

                            depth[x, y] = pix[index];

                            
                            if (depth[x, y] < iMin && depth[x, y] > 0)
                                iMin = depth[x, y];
                            if (depth[x, y] > iMax)
                                iMax = depth[x, y];

                        }
                    }
                }
            }
            finally { bmpexDepth.UnlockBits(); }

            //if (iMax > 1000)
            //    iMax = 1000;
            List<int> lDepths = new List<int>(dDepths.Keys);
            foreach(int iDepth in lDepths)
            {
                if (dDepths[iDepth] < 100)
                    dDepths.Remove(iDepth);
            }
            dDepths.Remove(0);
            iMin = dDepths.Keys.First() * 10;
            iMax = dDepths.Keys.Last() * 10;

            tbMin.Minimum = iMin;
            tbMin.Maximum = iMax;
            tbMin.SmallChange = 1;
            tbMin.TickStyle = TickStyle.Both;
            tbMaxDepth.Minimum = iMin;
            tbMaxDepth.Maximum = iMax;
            tbMaxDepth.SmallChange = 1;
            tbMaxDepth.TickStyle = TickStyle.Both;
            tbMaxDepth.Value = tbMaxDepth.Maximum;

        }




        void FilterPixels()
        {
            try
            {
                int iMinDepth = tbMin.Value;
                int iMaxDepth = tbMaxDepth.Value;
                LockBitmap bmpFiltered = new LockBitmap(bmp);
                bmpFiltered.LockBits();
                for (int i = 0; i < bmp.Width; i++)
                {
                    for (int j = 0; j < bmp.Height; j++)
                    {
                        Color cOrg = bmpFiltered.GetPixel(i, j);
                        int avg = (cOrg.R + cOrg.G + cOrg.B) / 3;
                        Color cGray = Color.FromArgb(avg, avg, avg);

                        if (depth[i, j] == 0)
                            bmpFiltered.SetPixel(i, j, Color.Blue);
                        else
                        {
                            if (depth[i, j] < iMinDepth || depth[i, j] > iMaxDepth)
                            {
                                if (chkBackground.Checked)
                                {
                                    bmpFiltered.SetPixel(i, j, Color.Black);
                                }
                                else
                                    bmpFiltered.SetPixel(i, j, cGray);

                            }
                        }
                    }
                }
                bmpFiltered.UnlockBits();
                //picRGB.Image = bmpFiltered;
                SetImage(picRGB, bmpFiltered);
                lblDepth.Text = "Depth range: " + tbMin.Value.ToString() + "-" + tbMaxDepth.Value;
            }
            catch(Exception ex)
            { }
        }

        public void SetImage(PictureBox pic, Image bmp)
        {
            
            Bitmap img = new Bitmap(bmp,
                        (int)(bmp.Width / m_dZoomscale),
                        (int)(bmp.Height / m_dZoomscale));
            pic.SizeMode = PictureBoxSizeMode.CenterImage;
            pic.Image = img;
           
        }

        private void TbMin_Scroll(object sender, EventArgs e)
        {
            if (tbMaxDepth.Value < tbMin.Value)
                tbMaxDepth.Value = tbMin.Value;
            FilterPixels();

        }

        private void TbMaxDepth_Scroll_1(object sender, EventArgs e)
        {
            if (tbMaxDepth.Value < tbMin.Value)
                tbMin.Value = tbMaxDepth.Value;
            FilterPixels();

        }

        private void PicRGB_MouseClick(object sender, MouseEventArgs e)
        {
            try
            {
                double iXScale = (bmp.Width * 1.0) / picRGB.Width;
                double iYScale = (bmp.Height * 1.0) / picRGB.Height;
                int x = (int)(e.Location.X * iXScale);
                int y = (int)(e.Location.Y * iYScale);
                if (depth[x, y] != 0)
                {
                    tbMaxDepth.Value = depth[x, y] + 5;
                    tbMin.Value = depth[x, y] - 5;
                    FilterPixels();
                }
                return;
            }
            catch (Exception ex)
            { }
        }

        private Matrix transform = new Matrix();
        private float m_dZoomscale = 1.0f;
        public const float s_dScrollValue = 0.1f;

        protected override void OnMouseWheel(MouseEventArgs mea)
        {
            picRGB.SizeMode = PictureBoxSizeMode.Normal;
            picRGB.Focus();
            if (picRGB.Focused == true && mea.Delta != 0)
            {
                // Map the Form-centric mouse location to the PictureBox client coordinate system
                Point pictureBoxPoint = picRGB.PointToClient(this.PointToScreen(mea.Location));
                ZoomScroll(pictureBoxPoint, mea.Delta > 0);
            }
        }
        private void ZoomScroll(Point location, bool zoomIn)
        {
            // Figure out what the new scale will be. Ensure the scale factor remains between
            // 1% and 1000%
            float newScale = Math.Min(Math.Max(m_dZoomscale + (zoomIn ? s_dScrollValue : -s_dScrollValue), 0.1f), 10);

            if (newScale != m_dZoomscale)
            {
                float adjust = newScale / m_dZoomscale;
                m_dZoomscale = newScale;

                FilterPixels();
                /*
                // Translate mouse point to origin
                transform.Translate(-location.X, -location.Y, MatrixOrder.Append);

                // Scale view
                transform.Scale(adjust, adjust, MatrixOrder.Append);

                // Translate origin back to original mouse point.
                transform.Translate(location.X, location.Y, MatrixOrder.Append);

                picRGB.Invalidate();
                */
            }
        }

        private void frmDepthAnalyzer_Load(object sender, EventArgs e)
        {
            //FormBorderStyle = FormBorderStyle.Sizable;
            WindowState = FormWindowState.Maximized;
            float widthRatio = Screen.PrimaryScreen.Bounds.Width / 1280;
            float heightRatio = Screen.PrimaryScreen.Bounds.Height / 800f;
            SizeF scale = new SizeF(widthRatio, heightRatio);
            this.Scale(scale);
        }

        private void radioZoomOut_CheckedChanged(object sender, EventArgs e)
        {
            //Zoom = ZoomMode.ZoomOut;
        }

        private void radioZoomIn_CheckedChanged(object sender, EventArgs e)
        {
            //Zoom = ZoomMode.ZoomIn;
        }

        private void radioNoZoom_CheckedChanged(object sender, EventArgs e)
        {
            //Zoom = ZoomMode.NoZoom;
        }

        private void picRGB_Paint(object sender, PaintEventArgs e)
        {
            /*
            if (bmp != null)
            {
                Graphics g = e.Graphics;
                g.Transform = transform;
                Pen mypen = new Pen(Color.Red, 5);
                Rectangle rect = new Rectangle(10, 10, 30, 30);
                g.DrawRectangle(mypen, rect);
            }
            */
        }

        private void chkBackground_CheckedChanged(object sender, EventArgs e)
        {

        }
    }
}
