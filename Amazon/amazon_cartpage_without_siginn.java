package Amazon.Project_maven;

import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.FindBy;
import org.openqa.selenium.support.PageFactory;

import Utility.data_fetching;

public class amazon_cartpage_without_siginn
{
	WebDriver driver;
	@FindBy(name="proceedToRetailCheckout")
	WebElement submit;
	
	public void proceed_checkout()
	{
		submit.click();
	}
	
	public amazon_cartpage_without_siginn(WebDriver driver)
	{
		PageFactory.initElements(driver,this);
	}
	
}
