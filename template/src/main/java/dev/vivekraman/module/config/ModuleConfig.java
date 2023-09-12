package dev.vivekraman.module.config;

import org.springdoc.core.models.GroupedOpenApi;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.PropertySource;

@Configuration
@PropertySource(value = "classpath:" + Constants.MODULE_NAME + ".properties")
public class ModuleConfig {
  @Bean
  public GroupedOpenApi moduleApiGroup() {
    return GroupedOpenApi.builder()
        .group(Constants.MODULE_NAME)
        .packagesToScan("dev.vivekraman.module.controller")
        .build();
  }
}
