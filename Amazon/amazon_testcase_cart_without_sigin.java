package Amazon.Project_maven;

import java.io.IOException;
import java.time.Duration;
import java.util.Iterator;
import java.util.Set;

import org.apache.poi.EncryptedDocumentException;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.firefox.FirefoxDriver;
import org.testng.Reporter;
import org.testng.annotations.Listeners;
import org.testng.annotations.Test;


@Listeners(amazon_testListener_class.class)
public class amazon_testcase_cart_without_sigin 
{
	WebDriver driver;
	@Test
	public void cart_without_signin() throws EncryptedDocumentException, IOException, InterruptedException
	{

		driver=new FirefoxDriver();
		driver.get("https://www.amazon.in");
		driver.manage().window().maximize();
		driver.manage().timeouts().implicitlyWait(Duration.ofSeconds(15));
	
		amazon_searchpage s1=new amazon_searchpage(driver);
		s1.search_tf();
		s1.search_button();
		amazon_product_details_page p1=new amazon_product_details_page(driver);
		p1.select_shoe();
		Set<String> p=driver.getWindowHandles();
		Iterator<String> pid=p.iterator();
		String parent_id=pid.next();
		String child_id=pid.next();
		driver.switchTo().window(child_id);
		amazon_cartpage c1=new amazon_cartpage(driver);
		c1.add_to_cart();
		amazon_cartpage_without_siginn w=new amazon_cartpage_without_siginn(driver);
		w.proceed_checkout();
		Reporter.log("testcase successfull");
	}
}
