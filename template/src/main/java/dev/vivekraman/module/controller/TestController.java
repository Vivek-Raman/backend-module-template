package dev.vivekraman.module.controller;

import dev.vivekraman.monolith.model.Response;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;
import reactor.core.publisher.Mono;
import reactor.core.scheduler.Scheduler;

@RestController
@RequiredArgsConstructor
public class TestController {
  private final Scheduler scheduler;

  @GetMapping
  public Mono<Response<Boolean>> test() {
    return Mono.just(Response.of(true))
        .subscribeOn(scheduler);
  }
}
