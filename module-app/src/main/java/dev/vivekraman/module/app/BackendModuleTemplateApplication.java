package dev.vivekraman.module.app; // TODO: update package path

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication(scanBasePackages = "dev.vivekraman.*")
public class BackendModuleTemplateApplication { // TODO: update class name
	public static void main(String[] args) {
		SpringApplication.run(BackendModuleTemplateApplication.class, args);
	}
}
