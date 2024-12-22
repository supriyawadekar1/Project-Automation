package Utility;

import java.io.FileInputStream;
import java.io.IOException;

import org.apache.poi.EncryptedDocumentException;
import org.apache.poi.ss.usermodel.Workbook;
import org.apache.poi.ss.usermodel.WorkbookFactory;

import Amazon.Project_maven.Launch_quit;
import Amazon.Project_maven.amazon_testListener_class;

public class data_fetching 
{
	public static String un;
	public static String pwd;
	public void fetch() throws EncryptedDocumentException, IOException, InterruptedException
	{
		FileInputStream f1=new FileInputStream("C:\\Users\\NILESH\\eclipse-workspace\\Project_maven\\Excel_sheet\\data1.xlsx");
		Workbook wb=WorkbookFactory.create(f1);
		un=wb.getSheet("Sheet1").getRow(1).getCell(0).getStringCellValue();
		pwd=wb.getSheet("Sheet1").getRow(1).getCell(1).getStringCellValue();
	}
}
