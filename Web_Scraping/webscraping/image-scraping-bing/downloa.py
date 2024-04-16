from bing_images import bing

bing.download_images("cat",
                      20,
                      output_dir="home/rodgers/Desktop/Web-Scraping/Learn Web_Scraping/freecode_webscraping/image-scraping-bing/cat",
                      pool_size=20,
                      file_type="png",
                      filters='+filterui:aspect-square+filterui:color2-bw',
                      force_replace=True)