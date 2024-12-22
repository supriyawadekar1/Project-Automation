package Amazon.Project_maven;

import java.io.IOException;

import org.apache.poi.EncryptedDocumentException;
import org.testng.annotations.Listeners;
import org.testng.annotations.Test;

import Utility.data_fetching;
@Listeners(amazon_testListener_class.class)
public class amazon_testcase_product_details extends Launch_quit
{
	@Test
	public void p_details() throws EncryptedDocumentException, IOException, InterruptedException
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
		//p1.product_details();
		
	}
}