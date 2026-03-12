package com.recomm.userservice.controller;


import com.recomm.userservice.dto.CreateUserRequestDTO;
import com.recomm.userservice.dto.UserResponseDTO;

import com.recomm.userservice.service.UserService;

import com.recomm.userservice.dto.LoginUserResponseDTO;
import com.recomm.userservice.dto.RatePlaceDTO;
import com.recomm.userservice.dto.UpdateUserDTO;


import java.util.List;
import java.util.Map;
import java.util.UUID;

import org.springframework.http.ResponseEntity;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PatchMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestHeader;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;


@RestController
@RequestMapping("/users")
public class UserController {
    private static final Logger logger = LoggerFactory.getLogger(UserController.class);
    private final UserService userService;

    public UserController(UserService userService){
        this.userService = userService;
    }

    //Get specific user entire details
    @GetMapping()
    public ResponseEntity<UserResponseDTO> getUser(@RequestHeader("X-Authenticated-User-Id") String userId) {
        UserResponseDTO user = userService.getUser(userId);
        logger.info("User {}",user);
        return ResponseEntity.ok().body(user);
    }

    @GetMapping("/exists")
    public ResponseEntity<LoginUserResponseDTO> getUserExists(@RequestHeader("X-Authenticated-User-Id") String userId) {
        LoginUserResponseDTO user = userService.getUserExists(userId);
        return ResponseEntity.ok().body(user); 
    }

    

    @PostMapping("/create")
    public ResponseEntity<UserResponseDTO> createUser(@RequestBody CreateUserRequestDTO userRequestDTO, @RequestHeader("X-Authenticated-User-Id") String userId) {
        UserResponseDTO userResponseDTO = userService.createUser(userId, userRequestDTO);
        
        return ResponseEntity.ok().body(userResponseDTO);
    }

    
    @PostMapping("/rate")
    public ResponseEntity<RatePlaceDTO> ratePlace(@RequestBody RatePlaceDTO ratePlaceDTO, @RequestHeader("X-Authenticated-User-Id") String userId) {
        RatePlaceDTO responseDTO = userService.ratePlace(userId, ratePlaceDTO);
        
        return ResponseEntity.ok().body(responseDTO);
    }

     @PatchMapping("/update")
    public ResponseEntity<Void> updateProfile(@RequestBody UpdateUserDTO updateRequestDTO, @RequestHeader("X-Authenticated-User-Id") String userId) {
       
        userService.updateProfile(userId, updateRequestDTO);


        return ResponseEntity.ok().build();
        
    }

}
