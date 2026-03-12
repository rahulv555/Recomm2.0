package com.recomm.recommservice.controller;
import java.util.List;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestHeader;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.recomm.recommservice.dto.RecommRequestDTO;
import com.recomm.recommservice.dto.RecommResponseDTO;
import com.recomm.recommservice.service.RecommService;

@RestController
@RequestMapping("/recomm")
public class RecommController {
private static final Logger logger = LoggerFactory.getLogger(RecommController.class);
private final RecommService recommService;

public RecommController(RecommService recommService){
    this.recommService = recommService;
}

//Get recommendation for the user
    @PostMapping()
    public ResponseEntity<RecommResponseDTO> getUser(@RequestHeader("X-Authenticated-User-Id") String userId,@RequestBody RecommRequestDTO dto ) {
        RecommResponseDTO recomms = recommService.getRecomm(userId, dto.getLatitude(), dto.getLongitude());
        return ResponseEntity.ok().body(recomms);
    }
}
