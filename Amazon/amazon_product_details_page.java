package Amazon.Project_maven;

import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.FindBy;
import org.openqa.selenium.support.PageFactory;
import org.testng.Assert;

import Utility.data_fetching;

public class amazon_product_details_page extends data_fetching
{
	WebDriver driver;
	@FindBy(xpath="(//div[@class='a-section aok-relative s-image-tall-aspect'])[4]")
	WebElement selected_shoe;
	
	@FindBy(xpath="(//label[@class='a-form-label'])[1]")
	WebElement details;
	
	public void select_shoe()
	{
		selected_shoe.click();
		
	}
	
	/*
	 * public void product_details() { Assert.assertEquals(details.isDisplayed(),
	 * true,"showing product details page");
	 * 
	 * }
	 */
	public amazon_product_details_page(WebDriver driver)
	{
		PageFactory.initElements(driver,this);
	}
}
