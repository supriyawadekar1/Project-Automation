package Amazon.Project_maven;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.FindBy;
import org.openqa.selenium.support.PageFactory;

import Utility.data_fetching;

public class amazon_search_with_filter extends data_fetching
{
	WebDriver driver;
	@FindBy(id="twotabsearchtextbox")
	WebElement searchtf;
	
	@FindBy(id="nav-search-submit-button")
	WebElement searchbtn;
	
	@FindBy(id="p_90/6741118031")
	WebElement checkbox1;
	
	@FindBy(linkText="Men's Shoes")
	WebElement wsneaker;
	
	@FindBy(id="p_72/1318476031")
	WebElement ratings;
	
	@FindBy(id="p_123/256097")
	WebElement brands;
	
	public void search_tf()
	{
		searchtf.sendKeys("shoe");
	}
	
	public void search_button()
	{
		searchbtn.click();
	}
	public void get_it_by_tomm()
	{
		checkbox1.click();
	}
	public void womens_sneaker()
	{
		wsneaker.click();
	}
	public void review()
	{
		ratings.click();
	}
	public void brand_selection()
	{
		brands.click();
	}
	amazon_search_with_filter(WebDriver driver)
	{
		PageFactory.initElements(driver,this);
	}
	
}
