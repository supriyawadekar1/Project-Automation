package Amazon.Project_maven;

import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.interactions.Actions;
import org.openqa.selenium.support.FindBy;
import org.openqa.selenium.support.PageFactory;

import Utility.data_fetching;

public class amazon_edit_profile extends data_fetching
{
	WebDriver driver;
	@FindBy(xpath="//span[@id='nav-link-accountList-nav-line-1']")
	WebElement hover_over;
	
	@FindBy(xpath="//button/div/span[.='Manage Profiles']")
	WebElement manage_profile;
	
	@FindBy(linkText="View")
	WebElement view_profile;
	
	@FindBy(className="editNameIcon")
	WebElement edit_name;
	
	
	public void hover() 
	{
		Actions a3=new Actions(driver);
		a3.moveToElement(hover_over).perform();
	}
	public void manage()
	{
		manage_profile.click();
	}
	public void viewprofile()
	{
		view_profile.click();
	}
	public void editname()
	{
		edit_name.click();
	}
	
	public amazon_edit_profile(WebDriver driver)
	{
		PageFactory.initElements(driver,this);
	}
	
}
