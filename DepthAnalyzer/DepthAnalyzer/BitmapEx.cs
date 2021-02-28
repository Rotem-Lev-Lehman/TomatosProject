using System;
using System.IO;
using System.Runtime.InteropServices;
using System.Windows.Media;
using System.Windows.Media.Imaging;

public class BitmapEx
{
    public int Width;
    public int Height;

    public int ChannelCount;
    public int BytesPerChannel;
    public bool HasAlpha;
    public int BitDepth;
    public bool IsBGR;
    public bool IsPinned;
    public IntPtr Scan0;

    private PixelFormat InputPixelFormat;
    private GCHandle pinHandle;
    private byte[] ImageData;


    /// <summary>
    /// Loads an image from a path. (Jpg, Png, Tiff, Bmp, Gif and Wdp are supported)
    /// </summary>
    /// <param name="path">Path to the image</param>
    public BitmapEx(string path)
    {
        using (Stream str = new FileStream(path, FileMode.Open, FileAccess.Read, FileShare.Read))
        {
            BitmapDecoder dec = BitmapDecoder.Create(str, BitmapCreateOptions.PreservePixelFormat, BitmapCacheOption.Default);
            if (dec.Frames.Count > 0) SetFromBitmapSource(dec.Frames[0]);
            else throw new FileLoadException("Couldn't load file " + path);
        }
    }

    /// <summary>
    /// Loads an image from an encoded stream. (Jpg, Png, Tiff, Bmp, Gif and Wdp are supported)
    /// </summary>
    public BitmapEx(Stream encodedStream)
    {
        encodedStream.Position = 0;
        BitmapDecoder dec = BitmapDecoder.Create(encodedStream,
            BitmapCreateOptions.PreservePixelFormat, BitmapCacheOption.Default);
        if (dec.Frames.Count > 0) SetFromBitmapSource(dec.Frames[0]);
        else throw new FileLoadException("Couldn't load file");
    }

    /// <summary>
    /// Loads an image from an encoded byte array. (Jpg, Png, Tiff, Bmp, Gif and Wdp are supported)
    /// </summary>
    public BitmapEx(byte[] encodedData)
    {
        using (MemoryStream str = new MemoryStream(encodedData))
        {
            BitmapDecoder dec = BitmapDecoder.Create(str,
                BitmapCreateOptions.PreservePixelFormat, BitmapCacheOption.Default);
            if (dec.Frames.Count > 0) SetFromBitmapSource(dec.Frames[0]);
            else throw new FileLoadException("Couldn't load file");
        }
    }

    private void SetFromBitmapSource(BitmapSource bmpSrc)
    {
        this.Width = bmpSrc.PixelWidth;
        this.Height = bmpSrc.PixelHeight;

        InputPixelFormat = bmpSrc.Format;
        if (bmpSrc.Format == PixelFormats.Bgr24)
        {
            this.ChannelCount = 3;
            this.BytesPerChannel = 1;
            this.HasAlpha = false;
            this.BitDepth = 8;
            this.IsBGR = true;
        }
        else if (bmpSrc.Format == PixelFormats.Bgra32)
        {
            this.ChannelCount = 4;
            this.BytesPerChannel = 1;
            this.HasAlpha = true;
            this.BitDepth = 8;
            this.IsBGR = true;
        }
        else if (bmpSrc.Format == PixelFormats.Rgb24)
        {
            this.ChannelCount = 3;
            this.BytesPerChannel = 1;
            this.HasAlpha = false;
            this.BitDepth = 8;
            this.IsBGR = false;
        }
        else if (bmpSrc.Format == PixelFormats.Rgb48)
        {
            this.ChannelCount = 3;
            this.BytesPerChannel = 2;
            this.HasAlpha = false;
            this.BitDepth = 16;
            this.IsBGR = false;
        }
        else if (bmpSrc.Format == PixelFormats.Gray16)
        {
            this.ChannelCount = 1;
            this.BytesPerChannel = 2;
            this.HasAlpha = false;
            this.BitDepth = 16;
            this.IsBGR = false;
        }
        else
        {
            //There are some more special cases you might want to handle
            //Also, it's possible that bmpSrc.Format == PixelFormats.Default
            //Then you can only check for BitsPerPixel field and guess the channel order (I assume it's BGR)
            throw new NotImplementedException();
        }

        int stride = this.Width * this.BytesPerChannel * this.ChannelCount;
        ImageData = new byte[this.Height * stride];
        bmpSrc.CopyPixels(ImageData, stride, 0);
    }

    public void LockBits()
    {
        if (!IsPinned)
        {
            pinHandle = GCHandle.Alloc(ImageData, GCHandleType.Pinned);
            Scan0 = pinHandle.AddrOfPinnedObject();
            IsPinned = true;
        }
    }

    public void UnlockBits()
    {
        if (IsPinned)
        {
            pinHandle.Free();
            IsPinned = false;
        }
    }

    /// <summary>
    /// Saves the image to a path. (Jpg, Png, Tiff, Bmp, Gif and Wdp are supported)
    /// </summary>
    /// <param name="path">Path where the image should be saved to</param>
    public void Save(string path)
    {
        string ext = Path.GetExtension(path).ToLower();
        using (FileStream str = new FileStream(path, FileMode.Create)) { this.Save(str, ext); }
    }

    /// <summary>
    /// Saves the image into a stream.
    /// </summary>
    /// <param name="ext">Extension of the desired file format. 
    /// Allowed values: ".jpg", ".jpeg", ".png", 
    /// ".tiff", ".tif", ".bmp", ".gif", ".wdp"</param>
    /// <param name="str">The stream where the image will be saved to.</param>
    public void Save(Stream str, string ext)
    {
        BitmapEncoder enc;
        switch (ext)
        {
            case ".jpg":
            case ".jpeg":
                enc = new JpegBitmapEncoder();
                ((JpegBitmapEncoder)enc).QualityLevel = 100; break;
            case ".tif":
            case ".tiff":
                enc = new TiffBitmapEncoder();
                ((TiffBitmapEncoder)enc).Compression = TiffCompressOption.Lzw; break;
            case ".png": enc = new PngBitmapEncoder(); break;
            case ".bmp": enc = new BmpBitmapEncoder(); break;
            case ".wdp": enc = new WmpBitmapEncoder(); break;

            default:
                throw new ArgumentException("File format not supported *" + ext);
        }

        BitmapSource src = BitmapSource.Create((int)this.Width, (int)this.Height, 96, 96,
        InputPixelFormat, null, ImageData, (int)(this.Width * this.BytesPerChannel * this.ChannelCount));
        enc.Frames.Add(BitmapFrame.Create(src));
        enc.Save(str);
    }
}