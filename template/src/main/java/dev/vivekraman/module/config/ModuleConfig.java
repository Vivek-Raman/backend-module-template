package dev.vivekraman.module.config;

import org.springdoc.core.models.GroupedOpenApi;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class ModuleConfig { // TODO: update class name
  @Bean
  public GroupedOpenApi moduleApiGroup() { // TODO: update method name
    return GroupedOpenApi.builder()
        .group(Constants.MODULE_NAME)
        .packagesToScan("dev.vivekraman.module.controller") // TODO: update package path
        .build();
  }
}
