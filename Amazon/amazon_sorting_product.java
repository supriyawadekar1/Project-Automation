package Amazon.Project_maven;

import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.FindBy;
import org.openqa.selenium.support.PageFactory;
import org.openqa.selenium.support.ui.Select;

import Utility.data_fetching;

public class amazon_sorting_product extends data_fetching
{
	WebDriver driver;
	@FindBy(xpath="//select[@name='s']")
	WebElement sort_option1;
	//WebElement sort_option2;
	//WebElement sort_option3;
	
	
	public void sorting_options()
	{
		Select s=new Select(sort_option1);
		s.selectByVisibleText("Newest Arrivals");
		//Select s1=new Select(sort_option2);
		//s1.selectByVisibleText("Price: Low to High");
		//Select s2=new Select(sort_option2);
		//s2.selectByVisibleText("Avg. Customer Review");
	}
	
	public amazon_sorting_product(WebDriver driver)
	{
		PageFactory.initElements(driver,this);
	}
	
}
