package Amazon.Project_maven;

import org.openqa.selenium.Keys;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.FindBy;
import org.openqa.selenium.support.PageFactory;
import org.testng.Assert;

import Utility.data_fetching;

public class amazon_registration extends data_fetching
{
	WebDriver edriver;
	//step 1

		@FindBy(xpath="//a[@id='createAccountSubmit']")
		WebElement new_Account;
		
		@FindBy(xpath="//input[@name='customerName']")
		WebElement name;

	    @FindBy(xpath="//input[@placeholder='Mobile number']")
	    WebElement mobile_number;

	    @FindBy(xpath="//input[@name='password']")
	   	WebElement password;

	   	@FindBy(xpath="//span[@id='auth-continue-announce']")
	   	WebElement verify_Phone_number;
	    
	    //step 2
	    	public void new_user()
	    {
	    	new_Account.click();
	    	Assert.assertNotEquals("Amazon Sign In", "Amazon Registration");
	    }
	    public void enter_username()
	    {
	    	name.sendKeys("supriya wadekar");
	    }
	    public void enter_user_mobile_number()
	    {
	    	mobile_number.sendKeys("9538184123");
	    }
	    public void enter_user_password()
	    {
	    	password.sendKeys("shop123@amazonin"+Keys.TAB.ENTER);
	    	
	    }
	    public void verify_phone_number()
	    {
	    	verify_Phone_number.click();
	    	
	    }
	    //step 3
	public amazon_registration(WebDriver driver)
	{
		PageFactory.initElements(driver, this);
		
	}

}
