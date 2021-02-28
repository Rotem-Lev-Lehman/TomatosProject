namespace DepthAnalyzer
{
    partial class frmDepthAnalyzer
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(frmDepthAnalyzer));
            this.chkBackground = new System.Windows.Forms.CheckBox();
            this.label2 = new System.Windows.Forms.Label();
            this.label1 = new System.Windows.Forms.Label();
            this.picOrg = new System.Windows.Forms.PictureBox();
            this.tbMaxDepth = new System.Windows.Forms.TrackBar();
            this.lblDepth = new System.Windows.Forms.Label();
            this.hScrollBar1 = new System.Windows.Forms.HScrollBar();
            this.tbMin = new System.Windows.Forms.TrackBar();
            this.btnLoad = new System.Windows.Forms.Button();
            this.picRGB = new System.Windows.Forms.PictureBox();
            ((System.ComponentModel.ISupportInitialize)(this.picOrg)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.tbMaxDepth)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.tbMin)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.picRGB)).BeginInit();
            this.SuspendLayout();
            // 
            // chkBackground
            // 
            this.chkBackground.AutoSize = true;
            this.chkBackground.Location = new System.Drawing.Point(780, 530);
            this.chkBackground.Name = "chkBackground";
            this.chkBackground.Size = new System.Drawing.Size(113, 17);
            this.chkBackground.TabIndex = 19;
            this.chkBackground.Text = "Black out of range";
            this.chkBackground.UseVisualStyleBackColor = true;
            this.chkBackground.CheckedChanged += new System.EventHandler(this.chkBackground_CheckedChanged);
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.Location = new System.Drawing.Point(12, 636);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(57, 13);
            this.label2.TabIndex = 18;
            this.label2.Text = "Max depth";
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Location = new System.Drawing.Point(12, 587);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(54, 13);
            this.label1.TabIndex = 17;
            this.label1.Text = "Min depth";
            // 
            // picOrg
            // 
            this.picOrg.BorderStyle = System.Windows.Forms.BorderStyle.Fixed3D;
            this.picOrg.Location = new System.Drawing.Point(754, 12);
            this.picOrg.Name = "picOrg";
            this.picOrg.Size = new System.Drawing.Size(700, 509);
            this.picOrg.SizeMode = System.Windows.Forms.PictureBoxSizeMode.StretchImage;
            this.picOrg.TabIndex = 16;
            this.picOrg.TabStop = false;
            // 
            // tbMaxDepth
            // 
            this.tbMaxDepth.Location = new System.Drawing.Point(92, 632);
            this.tbMaxDepth.Name = "tbMaxDepth";
            this.tbMaxDepth.Size = new System.Drawing.Size(571, 45);
            this.tbMaxDepth.TabIndex = 15;
            this.tbMaxDepth.Scroll += new System.EventHandler(this.TbMaxDepth_Scroll_1);
            // 
            // lblDepth
            // 
            this.lblDepth.AutoSize = true;
            this.lblDepth.Location = new System.Drawing.Point(846, 803);
            this.lblDepth.Name = "lblDepth";
            this.lblDepth.Size = new System.Drawing.Size(0, 13);
            this.lblDepth.TabIndex = 14;
            // 
            // hScrollBar1
            // 
            this.hScrollBar1.Location = new System.Drawing.Point(115, 530);
            this.hScrollBar1.Name = "hScrollBar1";
            this.hScrollBar1.Size = new System.Drawing.Size(10, 42);
            this.hScrollBar1.TabIndex = 13;
            // 
            // tbMin
            // 
            this.tbMin.Location = new System.Drawing.Point(92, 575);
            this.tbMin.Name = "tbMin";
            this.tbMin.Size = new System.Drawing.Size(571, 45);
            this.tbMin.TabIndex = 12;
            this.tbMin.Scroll += new System.EventHandler(this.TbMin_Scroll);
            // 
            // btnLoad
            // 
            this.btnLoad.Location = new System.Drawing.Point(780, 629);
            this.btnLoad.Name = "btnLoad";
            this.btnLoad.Size = new System.Drawing.Size(75, 23);
            this.btnLoad.TabIndex = 11;
            this.btnLoad.Text = "Load";
            this.btnLoad.UseVisualStyleBackColor = true;
            this.btnLoad.Click += new System.EventHandler(this.BtnLoad_Click);
            // 
            // picRGB
            // 
            this.picRGB.BorderStyle = System.Windows.Forms.BorderStyle.Fixed3D;
            this.picRGB.Location = new System.Drawing.Point(10, 12);
            this.picRGB.Name = "picRGB";
            this.picRGB.Size = new System.Drawing.Size(700, 509);
            this.picRGB.SizeMode = System.Windows.Forms.PictureBoxSizeMode.StretchImage;
            this.picRGB.TabIndex = 10;
            this.picRGB.TabStop = false;
            this.picRGB.Paint += new System.Windows.Forms.PaintEventHandler(this.picRGB_Paint);
            this.picRGB.MouseClick += new System.Windows.Forms.MouseEventHandler(this.PicRGB_MouseClick);
            // 
            // frmDepthAnalyzer
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(1460, 675);
            this.Controls.Add(this.chkBackground);
            this.Controls.Add(this.label2);
            this.Controls.Add(this.label1);
            this.Controls.Add(this.picOrg);
            this.Controls.Add(this.tbMaxDepth);
            this.Controls.Add(this.lblDepth);
            this.Controls.Add(this.hScrollBar1);
            this.Controls.Add(this.tbMin);
            this.Controls.Add(this.btnLoad);
            this.Controls.Add(this.picRGB);
            this.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedToolWindow;
            this.Icon = ((System.Drawing.Icon)(resources.GetObject("$this.Icon")));
            this.Name = "frmDepthAnalyzer";
            this.Text = "Depth Analyzer";
            this.Load += new System.EventHandler(this.frmDepthAnalyzer_Load);
            ((System.ComponentModel.ISupportInitialize)(this.picOrg)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.tbMaxDepth)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.tbMin)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.picRGB)).EndInit();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.CheckBox chkBackground;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.PictureBox picOrg;
        private System.Windows.Forms.TrackBar tbMaxDepth;
        private System.Windows.Forms.Label lblDepth;
        private System.Windows.Forms.HScrollBar hScrollBar1;
        private System.Windows.Forms.TrackBar tbMin;
        private System.Windows.Forms.Button btnLoad;
        private System.Windows.Forms.PictureBox picRGB;
    }
}

