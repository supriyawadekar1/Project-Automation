package Amazon.Project_maven;

import java.io.File;
import java.io.IOException;

import org.apache.commons.io.FileUtils;
import org.openqa.selenium.OutputType;
import org.openqa.selenium.TakesScreenshot;
import org.openqa.selenium.WebDriver;
import org.testng.ITestContext;
import org.testng.ITestListener;
import org.testng.ITestResult;
import org.testng.Reporter;

public class amazon_testListener_class implements ITestListener 
{
		static WebDriver driver;
		@Override
		public void onFinish(ITestContext context) {
			// TODO Auto-generated method stub
			ITestListener.super.onFinish(context);
			Reporter.log("Test suite successful");
		}

		@Override
		public void onStart(ITestContext context) {
			// TODO Auto-generated method stub
			ITestListener.super.onStart(context);
			Reporter.log("Test suite started");
		}

		@Override
		public void onTestFailedButWithinSuccessPercentage(ITestResult result) {
			// TODO Auto-generated method stub
			ITestListener.super.onTestFailedButWithinSuccessPercentage(result);
		}

		@Override
		public void onTestFailedWithTimeout(ITestResult result) {
			// TODO Auto-generated method stub
			ITestListener.super.onTestFailedWithTimeout(result);
			Reporter.log("Test case failed due to timeout exception");
		}

		@Override
		public void onTestFailure (ITestResult result) {
			// TODO Auto-generated method stub
			ITestListener.super.onTestFailure(result);
			
			TakesScreenshot ts=(TakesScreenshot) driver;
			File src=ts.getScreenshotAs(OutputType.FILE);
			File dstnt=new File("C:\\Users\\NILESH\\eclipse-workspace\\Project_maven_one\\Screenshot\\fail\\supriya"+Math.random()+".png");
			try {
				FileUtils.copyFile(src, dstnt);
			} catch (IOException e) {
				
				e.printStackTrace();
			}
			
			Reporter.log("Test case failed");
		}

		@Override
		public void onTestSkipped(ITestResult result) {
			// TODO Auto-generated method stub
			ITestListener.super.onTestSkipped(result);
			Reporter.log("Test case skipped");
		}

		@Override
		public void onTestStart(ITestResult result) {
			// TODO Auto-generated method stub
			ITestListener.super.onTestStart(result);
			Reporter.log("Test case started");
		}

		@Override
		public void onTestSuccess(ITestResult result) 
		{
			ITestListener.super.onTestSuccess(result);
			
			TakesScreenshot ts=(TakesScreenshot) driver;
			File src=ts.getScreenshotAs(OutputType.FILE);
			File dstnt=new File("C:\\Users\\NILESH\\eclipse-workspace\\Project_maven_one\\Screenshot\\pass\\supriya"+Math.random()+".png");
			try {
				FileUtils.copyFile(src, dstnt);
			} catch (IOException e) {
				
				e.printStackTrace();
			}
			
			Reporter.log("Test case successful");
		}

		
	

}
