package dev.vivekraman.module.app;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication(scanBasePackages = "dev.vivekraman.*")
public class BackendModuleTemplateApplication {
	public static void main(String[] args) {
		SpringApplication.run(BackendModuleTemplateApplication.class, args);
	}
}
