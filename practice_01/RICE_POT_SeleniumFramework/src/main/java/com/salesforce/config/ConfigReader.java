package com.salesforce.config;

import java.io.IOException;
import java.io.InputStream;
import java.util.Properties;

public class ConfigReader {

    private static final Properties PROPERTIES = new Properties();

    static {
        try (InputStream input = ConfigReader.class.getClassLoader()
                .getResourceAsStream("config.properties")) {
            if (input == null) {
                throw new IllegalStateException("config.properties not found in classpath");
            }
            PROPERTIES.load(input);
        } catch (IOException e) {
            throw new ExceptionInInitializerError(e);
        }
    }

    private ConfigReader() {
    }

    public static String getProperty(String key) {
        return PROPERTIES.getProperty(key);
    }

    public static String getBaseUrl() {
        return PROPERTIES.getProperty("base.url");
    }

    public static String getBrowser() {
        return PROPERTIES.getProperty("browser");
    }

    public static String getValidUsername() {
        return PROPERTIES.getProperty("valid.username");
    }

    public static String getValidPassword() {
        return PROPERTIES.getProperty("valid.password");
    }

    public static int getWaitTimeout() {
        return Integer.parseInt(PROPERTIES.getProperty("wait.timeout"));
    }

    public static int getPageLoadTimeout() {
        return Integer.parseInt(PROPERTIES.getProperty("page.load.timeout"));
    }
}
