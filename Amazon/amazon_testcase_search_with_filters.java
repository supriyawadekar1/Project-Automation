package Amazon.Project_maven;

import java.io.IOException;

import org.apache.poi.EncryptedDocumentException;
import org.testng.annotations.Listeners;
import org.testng.annotations.Test;

import Utility.data_fetching;
@Listeners(amazon_testListener_class.class)
public class amazon_testcase_search_with_filters extends Launch_quit 
{
	@Test
	public void amazon_search_with_filter() throws EncryptedDocumentException, IOException, InterruptedException
	{
		data_fetching d1=new data_fetching();
		d1.fetch();
		amazon_loginpage a1=new amazon_loginpage(driver);//invoke constructor
		a1.uname();
		a1.cbutton();
		a1.valid_pswd();
		a1.signin();
		amazon_search_with_filter s1=new amazon_search_with_filter(driver);
		s1.search_tf();
		s1.search_button();
		s1.get_it_by_tomm();
		s1.womens_sneaker();
		s1.review();
		s1.brand_selection();
		
	}
}
