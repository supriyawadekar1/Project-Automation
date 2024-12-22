package Amazon.Project_maven;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.FindBy;
import org.openqa.selenium.support.PageFactory;
import org.openqa.selenium.support.ui.Select;

import Utility.data_fetching;

public class amazon_checkout extends data_fetching
{
	WebDriver driver;
	@FindBy(name="proceedToRetailCheckout")
	WebElement proceed_tobuy;
	
	@FindBy(xpath="//input[@class='a-button-input'])[2]")
	WebElement usethis_addr;
	
	@FindBy(xpath="//input[@value='SelectableAddCreditCard']")
	WebElement radio_button;
	
	@FindBy(linkText="Enter card details")
	WebElement enter_details;
	
	@FindBy(name="ApxSecureIframe")
	WebElement frame;
	
	@FindBy(name="addCreditCardNumber")
	WebElement card_no;
	
	@FindBy(xpath="//select[@name='ppw-expirationDate_month']")
	WebElement month;
	
	@FindBy(xpath="//select[@name='ppw-expirationDate_year']")
	WebElement year;
	
	@FindBy(xpath="//span/span/span[.='Enter card details']")
	WebElement enter_card;
	
	public void checkout_product()
	{
		proceed_tobuy.click();
		usethis_addr.click();
		radio_button.click();
		enter_details.click();
		WebElement frame=driver.findElement(By.name("ApxSecureIframe"));
		driver.switchTo().frame(frame);
		card_no.sendKeys("6522667101492090");
		Select sel=new Select(month);
		sel.selectByVisibleText("08");
		Select sel1=new Select(year);
		sel1.selectByVisibleText("2025");
		enter_card.click();
		
	}
	public amazon_checkout(WebDriver driver)
	{
		PageFactory.initElements(driver,this);
	}

}
