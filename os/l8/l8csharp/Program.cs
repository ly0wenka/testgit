using System;
using System.IO;
using System.Linq;
using DocumentFormat.OpenXml;
using DocumentFormat.OpenXml.Packaging;
using DocumentFormat.OpenXml.Wordprocessing;

class Program
{
    static void Main()
    {
        string folder = @"S:\Users\L\Downloads\New folder (175)\testgit\os\l8\imgs";
        string output = Path.Combine(folder, "imgs.docx");

        var images = Directory.GetFiles(folder)
            .Where(f => new[] { ".png", ".jpg", ".jpeg", ".bmp", ".gif" }
            .Contains(Path.GetExtension(f).ToLower()))
            .OrderBy(f => f)
            .ToList();

        using (WordprocessingDocument doc =
            WordprocessingDocument.Create(output, WordprocessingDocumentType.Document))
        {
            MainDocumentPart main = doc.AddMainDocumentPart();
            main.Document = new Document(new Body());
            Body body = main.Document.Body;

            int index = 1;

            foreach (var imgPath in images)
            {
                string fileName = Path.GetFileNameWithoutExtension(imgPath);

                // 1. Reference text
                body.Append(
                    new Paragraph(
                        new Run(new Text($"На рис. {index} зображено {fileName}.")))
                );

                // 2. Add image
                ImagePart imagePart = main.AddImagePart(ImagePartType.Jpeg);
                using (FileStream fs = new FileStream(imgPath, FileMode.Open))
                    imagePart.FeedData(fs);

                string relId = main.GetIdOfPart(imagePart);

                var drawing = CreateImage(relId);
                body.Append(new Paragraph(new Run(drawing)));

                // 3. Caption
                body.Append(
                    new Paragraph(
                        new Run(new Text($"Рис. {index} — {fileName}")))
                );

                index++;
            }
        }

        Console.WriteLine("Готово: " + output);
    }

    static Drawing CreateImage(string relationshipId)
    {
        return new Drawing(
            new DocumentFormat.OpenXml.Drawing.Wordprocessing.Inline(
                new DocumentFormat.OpenXml.Drawing.Wordprocessing.Extent() { Cx = 5000000, Cy = 3500000 },
                new DocumentFormat.OpenXml.Drawing.Graphic(
                    new DocumentFormat.OpenXml.Drawing.GraphicData(
                        new DocumentFormat.OpenXml.Drawing.Pictures.Picture(
                            new DocumentFormat.OpenXml.Drawing.Pictures.NonVisualPictureProperties(
                                new DocumentFormat.OpenXml.Drawing.Pictures.NonVisualDrawingProperties() { Id = 1, Name = "Image" },
                                new DocumentFormat.OpenXml.Drawing.Pictures.NonVisualPictureDrawingProperties()
                            ),
                            new DocumentFormat.OpenXml.Drawing.Pictures.BlipFill(
                                new DocumentFormat.OpenXml.Drawing.Blip() { Embed = relationshipId },
                                new DocumentFormat.OpenXml.Drawing.Stretch(new DocumentFormat.OpenXml.Drawing.FillRectangle())
                            ),
                            new DocumentFormat.OpenXml.Drawing.Pictures.ShapeProperties(
                                new DocumentFormat.OpenXml.Drawing.Transform2D(
                                    new DocumentFormat.OpenXml.Drawing.Offset() { X = 0, Y = 0 },
                                    new DocumentFormat.OpenXml.Drawing.Extents() { Cx = 5000000, Cy = 3500000 }
                                ),
                                new DocumentFormat.OpenXml.Drawing.PresetGeometry(
                                    new DocumentFormat.OpenXml.Drawing.AdjustValueList()
                                ) { Preset = DocumentFormat.OpenXml.Drawing.ShapeTypeValues.Rectangle }
                            )
                        )
                    ) { Uri = "http://schemas.openxmlformats.org/drawingml/2006/picture" }
                )
            )
        );
    }
}