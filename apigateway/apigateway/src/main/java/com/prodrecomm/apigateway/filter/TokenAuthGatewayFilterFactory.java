package com.prodrecomm.apigateway.filter;

import java.net.http.HttpHeaders;
import com.google.firebase.FirebaseApp;
import com.google.firebase.FirebaseOptions;
import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.auth.FirebaseAuthException;
import com.google.firebase.auth.FirebaseToken;
import org.springframework.cloud.gateway.filter.GatewayFilter;
import org.springframework.cloud.gateway.filter.factory.AbstractGatewayFilterFactory;
import org.springframework.http.HttpStatus;
import org.springframework.http.server.reactive.ServerHttpRequest;
import org.springframework.stereotype.Component;
import org.springframework.web.server.ServerWebExchange;
import reactor.core.publisher.Mono;
import org.springframework.core.io.ClassPathResource;

import javax.annotation.PostConstruct;
import java.io.FileInputStream;
import java.io.IOException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
@Component
public class TokenAuthGatewayFilterFactory extends AbstractGatewayFilterFactory<Object> {

    
private static final Logger logger = LoggerFactory.getLogger(TokenAuthGatewayFilterFactory.class);


    @PostConstruct
    public void init() throws IOException {
        if (FirebaseApp.getApps().isEmpty()) {
            FirebaseOptions options = FirebaseOptions.builder()
                    .setCredentials(com.google.auth.oauth2.GoogleCredentials
                            .fromStream(new ClassPathResource("firebase-service-account.json").getInputStream()))
                    .build();
            FirebaseApp.initializeApp(options);
        }
    }

    @Override
    public GatewayFilter apply(Object config) {
        return (exchange, chain) -> {
        String authHeader = exchange.getRequest().getHeaders().getFirst("Authorization");

        if (authHeader == null || !authHeader.startsWith("Bearer ")) {
            return unauthorized(exchange, "Missing token");
        }

        String idToken = authHeader.substring(7);

        return Mono.fromCallable(() ->
        FirebaseAuth.getInstance().verifyIdToken(idToken)
    )
    .subscribeOn(reactor.core.scheduler.Schedulers.boundedElastic())
    .flatMap(decodedToken -> {
        logger.info("User ID access : {}",decodedToken.getUid());

        ServerHttpRequest mutated = exchange.getRequest().mutate()
                .header("X-Authenticated-User-Id", decodedToken.getUid())
                .header("X-Authenticated-User-Email", decodedToken.getEmail())
                .headers(headers -> headers.remove("Authorization")) //removing the token from the headers for security?
                .build();

        return chain.filter(exchange.mutate().request(mutated).build());
    })
    .onErrorResume(e -> unauthorized(exchange, "Invalid Firebase Token" + e));
};
    }

    private Mono<Void> unauthorized(ServerWebExchange exchange, String message) {
        exchange.getResponse().setStatusCode(HttpStatus.UNAUTHORIZED);

        
        logger.error(message);
        
        return exchange.getResponse().setComplete();
    }

    
}

