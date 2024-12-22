package Amazon.Project_maven;

import java.io.IOException;

import org.apache.poi.EncryptedDocumentException;
import org.testng.annotations.Test;

import Utility.data_fetching;

public class amazon_testcase_registration extends Launch_quit
{
	@Test
	public void amazon_newuser() throws EncryptedDocumentException, IOException, InterruptedException
	{
		data_fetching d1=new data_fetching();
		d1.fetch();
		amazon_registration r1=new amazon_registration(driver);
		r1.new_user();
		r1.enter_username();
		r1.enter_user_mobile_number();
		r1.enter_user_password();
		r1.verify_phone_number();
	}
}
