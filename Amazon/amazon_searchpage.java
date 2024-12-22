package Amazon.Project_maven;

import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.FindBy;
import org.openqa.selenium.support.PageFactory;

import Utility.data_fetching;

public class amazon_searchpage extends data_fetching
{
		WebDriver driver;
		@FindBy(id="twotabsearchtextbox")
		WebElement searchtf;
		
		@FindBy(id="nav-search-submit-button")
		WebElement searchbtn;
		
		public void search_tf()
		{
			searchtf.sendKeys("shoe");
		}
		
		public void search_button()
		{
			searchbtn.click();
		}
		
		public amazon_searchpage(WebDriver driver)
		{
			PageFactory.initElements(driver,this);
		}
		
		
}
