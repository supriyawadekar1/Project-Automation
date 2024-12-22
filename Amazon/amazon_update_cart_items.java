package Amazon.Project_maven;

import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.FindBy;
import org.openqa.selenium.support.PageFactory;
import org.openqa.selenium.support.ui.Select;

import Utility.data_fetching;

public class amazon_update_cart_items extends data_fetching
{
	WebDriver driver;
	@FindBy(linkText="Go to Cart")
	WebElement gotocart;
	
	@FindBy(xpath="//select[@name='quantity']")
	WebElement dropdown;
	
	@FindBy(xpath="(//input[@class='a-color-link'])[1]")
	WebElement delete;
	
	public void go_to_cart()
	{
		gotocart.click();
	}
	public void items_count_dd()
	{
		Select sel=new Select(dropdown);
		sel.selectByValue("3");
	}
	public void delete_items()
	{
		delete.click();
	}
	
	public amazon_update_cart_items(WebDriver driver)
	{
		PageFactory.initElements(driver,this);
	}
}
