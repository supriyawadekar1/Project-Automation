package Amazon.Project_maven;

import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.FindBy;
import org.openqa.selenium.support.PageFactory;

import Utility.data_fetching;

public class amazon_cartpage extends data_fetching
{
	WebDriver driver;
	@FindBy(xpath="//input[@value='Add to Cart']")
	WebElement add;
	
	public void add_to_cart()
	{
		add.click();
	}
	
	amazon_cartpage(WebDriver driver)
	{
		PageFactory.initElements(driver,this);
	}
	
}
