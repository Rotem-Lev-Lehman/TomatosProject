using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Drawing.Imaging;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace CropPlants
{
    public partial class frmCropPlants : Form
    {

        List<Rectangle> Rectangles;
        Rectangle CurrentRectangle;
        Point StartPoint, CurrentPoint;
        Bitmap bmp;
        bool MouseDown;
        List<FileInfo> Files;
        int CurrentFile;
        Dictionary<FileInfo, List<FileInfo>> CroppedFiles;
        private double XRatio, YRatio;

        public frmCropPlants()
        {
            InitializeComponent();
            MouseDown = false;
            CurrentRectangle = new Rectangle(-1,-1,0,0);
            pictureBox1.SizeMode = PictureBoxSizeMode.StretchImage;
            txtPath.Text = @"C:\Users\shanigu\Downloads\images";
            txtTargetDir.Text = @"C:\Users\shanigu\Downloads\images\Cropped";
            Rectangles = new List<Rectangle>();
            CroppedFiles = new Dictionary<FileInfo, List<FileInfo>>();
        }

        private void pictureBox1_Paint(object sender, PaintEventArgs e)
        {
            Graphics g = e.Graphics;
            for (int i = 0; i < Rectangles.Count; i++)
            {
                if (i == lstRectangles.SelectedIndex)
                    g.DrawRectangle(Pens.Orange, Rectangles[i]);
                else
                    g.DrawRectangle(Pens.Red, Rectangles[i]);
            }
            if (CurrentRectangle.X > 0)
                g.DrawRectangle(Pens.Red, CurrentRectangle);
        }

        private void pictureBox1_MouseDown(object sender, MouseEventArgs e)
        {
            MouseDown = true;
            CurrentRectangle = new Rectangle(e.X, e.Y, 50, 50);
            StartPoint = new Point(e.X, e.Y);
            CurrentPoint = new Point(e.X + 50, e.Y + 50);
        }

        private void pictureBox1_MouseUp(object sender, MouseEventArgs e)
        {
            MouseDown = false;
            Rectangles.Add(CurrentRectangle);
            CurrentRectangle = new Rectangle(-1, -1, 0, 0);
            WriteRectangles();
        }

        private void pictureBox1_MouseMove(object sender, MouseEventArgs e)
        {
            if (MouseDown == true)
            {
                
                if (e.Y < pictureBox1.Height && e.Y > 0)
                    CurrentPoint.Y = e.Y;
                if (e.X < pictureBox1.Width && e.X > 0)
                    CurrentPoint.X = e.X;

                if (StartPoint.X < CurrentPoint.X)
                {
                    CurrentRectangle.X = StartPoint.X;
                    CurrentRectangle.Width = CurrentPoint.X - StartPoint.X;
                }
                else
                {
                    CurrentRectangle.X = CurrentPoint.X;
                    CurrentRectangle.Width = StartPoint.X - CurrentPoint.X;
                }
                if (StartPoint.Y < CurrentPoint.Y)
                {
                    CurrentRectangle.Y = StartPoint.Y;
                    CurrentRectangle.Height = CurrentPoint.Y - StartPoint.Y;
                }
                else
                {
                    CurrentRectangle.Y = CurrentPoint.Y;
                    CurrentRectangle.Height = StartPoint.Y - CurrentPoint.Y;
                }


                Refresh();
            }
        }

        protected override bool ProcessCmdKey(ref Message msg, Keys keyData)
        {
            if (keyData == Keys.Delete)
                OnKeyPress(new KeyPressEventArgs((Char)Keys.Delete));
            return base.ProcessCmdKey(ref msg, keyData);
        }

        public void WriteRectangles()
        {
            lstRectangles.Items.Clear();
            foreach (Rectangle r in Rectangles)
                lstRectangles.Items.Add("[" + r.X + "," + r.Y + "," + (r.X + r.Width) + "," + (r.Y + r.Height) + "]");
            lstRectangles.SelectedIndex = Rectangles.Count - 1;
        }

        private void DeleteSelectedRectangle()
        {
            if (Rectangles.Count > 0 && lstRectangles.SelectedIndex >= 0)
            {
                Rectangles.RemoveAt(lstRectangles.SelectedIndex);
                WriteRectangles();
                Refresh();
            }
        }

        private void Form1_KeyPress(object sender, KeyPressEventArgs e)
        {
            if (e.KeyChar == (Char)Keys.Delete)
            {
                DeleteSelectedRectangle();
            }
        }

        private void Form1_Load(object sender, EventArgs e)
        {
            MinimizeBox = false;
            MaximizeBox = false;
            FormBorderStyle = FormBorderStyle.FixedSingle;
        }

        private void btnLoad_Click(object sender, EventArgs e)
        {
            InNext = true;
            try
            {
                DirectoryInfo dir = new DirectoryInfo(txtPath.Text);
                lstFiles.ClearSelected();
                lstFiles.Items.Clear();
                Files = new List<FileInfo>();
                PopulateList(dir);
                lblFiles.Text = "Files (" + Files.Count + "):";
                foreach (FileInfo fi in Files)
                    lstFiles.Items.Add(fi.Name);
                CurrentFile = 0;
                if(Files.Count > 0)
                {
                    LoadImage();
                    lstFiles.SelectedIndex = CurrentFile;

                    Rectangles = new List<Rectangle>();
                }
            }
            catch(Exception ex)
            {

            }
            InNext = false;
        }

        

        private void PopulateList(DirectoryInfo dir)
        {
            foreach(FileInfo file in dir.GetFiles())
            {
                if(file.Extension.ToLower().Contains("png" ))
                {
                    if (file.Name.ToLower().Contains("_color_"))
                        Files.Add(file);
                }
            }
            foreach (DirectoryInfo dSub in dir.GetDirectories())
                PopulateList(dSub);
        }


        public  Bitmap CropAtRect(Bitmap b, Rectangle r)
        {
            Bitmap nb = new Bitmap((int)(r.Width * XRatio), (int)(r.Height * YRatio));
            using (Graphics g = Graphics.FromImage(nb))
            {
                g.DrawImage(b, (int)-(r.X * XRatio), (int)-(r.Y * YRatio));
                return nb;
            }
        }

        bool InNext = false;

        private void SaveRectangles()
        {
            try
            {
                string sTargetDir = txtTargetDir.Text;
                string sJPEGDir = sTargetDir + "/JPEGS";
                if (!Directory.Exists(sTargetDir))
                    Directory.CreateDirectory(sTargetDir);
                if (!Directory.Exists(sJPEGDir))
                    Directory.CreateDirectory(sJPEGDir);

                StreamWriter sw = new StreamWriter(sTargetDir + "/Rectangles.txt", true);
                string sLine = Files[CurrentFile].FullName + "\t" + Rectangles.Count;
                foreach (Rectangle r in Rectangles)
                    sLine += "\t [" + r.X + "," + r.Y + "," + (r.X + r.Width) + "," + (r.Y + r.Height) + "]";
                sw.WriteLine(sLine);
                sw.Close();

                foreach (Rectangle r in Rectangles)
                {
                    Bitmap bmpCropped = CropAtRect(bmp, r);
                    string sFileName = Files[CurrentFile].Name.Replace(".png", "") + "_" + r.X + "_" + r.Y + "_" + (r.X + r.Width) + "_" + (r.Y + r.Height);
                    bmpCropped.Save(sTargetDir + "\\" + sFileName + ".png");
                    bmpCropped.Save(sJPEGDir + "\\" + sFileName + ".jpeg", ImageFormat.Jpeg);
                }

                lstFiles.Items[CurrentFile] = "v " + lstFiles.Items[CurrentFile];
            }
            catch (Exception ex)
            {

            }
        }

        private void btnNext_Click(object sender, EventArgs e)
        {
            InNext = true;
            try
            {
                SaveRectangles();

                CurrentFile++;
                if (CurrentFile < Files.Count)
                {
                    lstFiles.SelectedIndex = CurrentFile;
                    LoadImage();
                    Rectangles = new List<Rectangle>();
                    lstRectangles.Items.Clear();
                }

            }
            catch (Exception ex)
            {

            }
            InNext = false;
        }

        private void lstFiles_SelectedIndexChanged(object sender, EventArgs e)
        {
            if(!InNext)
            {
                SaveRectangles();
                CurrentFile = lstFiles.SelectedIndex;
                LoadImage();
                Rectangles = new List<Rectangle>();
                lstRectangles.Items.Clear();
            }
        }

        private void lstRectangles_SelectedIndexChanged(object sender, EventArgs e)
        {
            Refresh();
        }

        private void btnDelete_Click(object sender, EventArgs e)
        {
            DeleteSelectedRectangle();
        }

        private void LoadImage()
        {
            bmp = new Bitmap(Files[CurrentFile].FullName);
            pictureBox1.Image = bmp;
            XRatio = (1.0 * bmp.Width) / pictureBox1.Width;
            YRatio = (1.0 * bmp.Height) / pictureBox1.Height;
        }
    }
}
