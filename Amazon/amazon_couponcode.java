package Amazon.Project_maven;

import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.interactions.Actions;
import org.openqa.selenium.support.FindBy;
import org.openqa.selenium.support.PageFactory;
import org.openqa.selenium.support.ui.Select;

import Utility.data_fetching;

public class amazon_couponcode extends data_fetching
{
	WebDriver driver;
	@FindBy(name="proceedToRetailCheckout")
	WebElement proceed_tobuy;
	
	@FindBy(xpath="(//input[@class='a-button-input'])[2]")
	WebElement usethis_addr;
	
	@FindBy(xpath="(//input[@name='ppw-instrumentRowSelection'])[2]")
	WebElement radio;
	
	@FindBy(xpath="(//span[@role='radio'])[1]")
	WebElement net;
	
	@FindBy(name="ApxSecureIframe")
	WebElement frame1;
	
	@FindBy(name="ppw-bankSelection_dropdown")
	WebElement net_dd;
	
	@FindBy(xpath="//span[.='Use this payment method']")
	WebElement use_this;
	
	@FindBy(id="spc-gcpromoinput")
	WebElement code_tf;
	
	@FindBy(xpath="(//span[@class='a-declarative'])[9]")
	WebElement apply_button;
	
	public void apply_coupon_code()
	{
		proceed_tobuy.click();
		usethis_addr.click();
		radio.click();
		net.click();
		driver.switchTo().frame(frame1);
		Select s1=new Select(net_dd);
		s1.selectByVisibleText("HDFC Bank");
		use_this.click();
		code_tf.sendKeys("Mychoice@123");
		apply_button.click();
	}
	
	
	public amazon_couponcode(WebDriver driver)
	{
		PageFactory.initElements(driver,this);
	}
	
}
