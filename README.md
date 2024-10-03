# Web-Crawler-Practice
This program was developed primarily based on the **Scrapy** framework, the **Beautiful Soup** parsing tool, **Lua** scripts, and the **Splash** service for rendering JavaScript, to scrape dynamically rendered table data from web pages.<br><br>
**Third-party Libraries**:  
- scrapy  
- bs4  
- scrapy_splash  
- pandas  
- matplotlib.pyplot  

**Requirements**:  
- Install Docker  
- SimSun Font Library  

**Steps to Use**:  

1. **Start scrapy_splash with Docker**:  
   Execute the following commands in the terminal to pull the Splash image and start the service on port 8050.

   ```bash
   docker pull scrapinghub/splash
   docker run -p 8050:8050 scrapinghub/splash
   ```
2. **Access Splash in the browser**:  
   Visit ```http://localhost:8050/``` in your browser to ensure the Splash service is running properly.

3. **Run the Scrapy Spider**:  
   Open the terminal, navigate to the ```myProject``` directory, and run the following command to execute the spider.

    ```bash
   scrapy crawl rateSpider
   ```
