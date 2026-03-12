package com.recomm.recommservice.service;

import java.util.List;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpStatusCode;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;

import com.recomm.recommservice.dto.RecommRequestDTO;
import com.recomm.recommservice.dto.RecommResponseDTO;

import reactor.core.publisher.Mono;

@Service
public class RecommService {
    private static final Logger logger = LoggerFactory.getLogger(RecommService.class);
    private final WebClient webClient;
    private final String mlServiceUrl;

    public RecommService(
            WebClient.Builder webClientBuilder, 
            @Value("${ml.service.url:http://ml-service:8088}") String mlServiceUrl) {
        
        this.mlServiceUrl = "http://ml-service:8088";
        // this.webClient = webClientBuilder.baseUrl(mlServiceUrl).build(); // Build a generic client
        // this.webClient = WebClient.create(this.mlServiceUrl);
        this.webClient = WebClient.builder().baseUrl(this.mlServiceUrl).build();
        logger.info("Service initialized with ML URL: {}", this.mlServiceUrl);
    }
    public RecommResponseDTO getRecomm(String userId, Double latitude, Double longitude){
        
        RecommRequestDTO dto = new RecommRequestDTO();
        dto.setLatitude(latitude);
        dto.setLongitude(longitude);
        return this.webClient.post()
                .uri(uriBuilder -> uriBuilder
                    .path("/recommend")
                    .queryParam("user_id", userId)
                    .build())
                .bodyValue(dto)
                .retrieve()
                .onStatus(HttpStatusCode::isError, response -> response.bodyToMono(String.class).flatMap(body -> {
            System.out.println("FastAPI Error Detail: " + body);
            return Mono.error(new RuntimeException(body));
        }))
                .bodyToMono(RecommResponseDTO.class)
                .block(); // not async
    }

    public void notifyInteraction() {
        
        this.webClient.post()
                .uri("/liketrain")
                .retrieve()
                .toBodilessEntity()
                .subscribe(success -> logger.info("Successfully notified ML for interaction"),
                error -> logger.error("Failed to notify ML: {}", error)); // Fire and forget
    }

    public void notifyUserUpdate(String userId) {
        
        this.webClient.post()
                .uri(uriBuilder -> uriBuilder
                    .path("/usertrain")
                    .queryParam("user_id", userId)
                    .build())
                .retrieve()
                .toBodilessEntity()
                .subscribe(success -> logger.info("Successfully notified ML for user: {}", userId),
                error -> logger.error("Failed to notify ML: {}", error)); 
    }

}
