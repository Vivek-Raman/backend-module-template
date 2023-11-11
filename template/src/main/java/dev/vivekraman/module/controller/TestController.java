package dev.vivekraman.module.controller;

import dev.vivekraman.module.config.Constants;
import dev.vivekraman.monolith.annotation.MonolithController;
import dev.vivekraman.monolith.model.Response;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.GetMapping;
import reactor.core.publisher.Mono;
import reactor.core.scheduler.Scheduler;

@MonolithController(moduleName = Constants.MODULE_NAME)
@RequiredArgsConstructor
public class TestController {
  private final Scheduler scheduler;

  @GetMapping
  public Mono<Response<Boolean>> test() {
    return Mono.just(Response.of(true))
        .subscribeOn(scheduler);
  }
}
