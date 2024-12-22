package Amazon.Project_maven;

import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.FindBy;
import org.openqa.selenium.support.PageFactory;

import Utility.data_fetching;

public class amazon_loginpage extends data_fetching
{
	WebDriver driver;
	//step1
	@FindBy(id="ap_email")
	WebElement username;
	
	@FindBy(xpath="//input[@id='continue']")
	WebElement continue_btn;
	
	@FindBy(id="ap_password")
	WebElement password;
	
	@FindBy(id="signInSubmit")
	WebElement signin_btn;
	//step2
	public void uname()
	{
		username.sendKeys(un);
	}
	
	public void cbutton()
	{
		continue_btn.click();
	}
	public void valid_pswd()
	{
		password.sendKeys(pwd);
	}
	public void invalid_pswd()
	{
		password.sendKeys("nsgjh1123");
	}
	public void signin()
	{
		signin_btn.click();
	}
	//step 3
	public amazon_loginpage(WebDriver driver) 
	{
		PageFactory.initElements(driver,this);
	}
}
