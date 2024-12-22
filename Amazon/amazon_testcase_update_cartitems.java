package Amazon.Project_maven;

import java.io.IOException;
import java.util.Iterator;
import java.util.Set;

import org.apache.poi.EncryptedDocumentException;
import org.testng.annotations.Listeners;
import org.testng.annotations.Test;

import Utility.data_fetching;
@Listeners(amazon_testListener_class.class)
public class amazon_testcase_update_cartitems extends Launch_quit
{
	@Test
	public void update_items() throws EncryptedDocumentException, IOException, InterruptedException
	{
		data_fetching d1=new data_fetching();
		d1.fetch();
		amazon_loginpage a1=new amazon_loginpage(driver);//invoke constructor
		a1.uname();
		a1.cbutton();
		a1.valid_pswd();
		a1.signin();
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
		amazon_update_cart_items u1=new amazon_update_cart_items(driver);
		u1.go_to_cart();
		u1.items_count_dd();
		u1.delete_items();
	}
}
