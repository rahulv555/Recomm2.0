package com.recomm.userservice.service;


import com.recomm.userservice.dto.CreateUserRequestDTO;
import com.recomm.userservice.dto.LoginUserResponseDTO;
import com.recomm.userservice.dto.RatePlaceDTO;
import com.recomm.userservice.dto.UpdateUserDTO;
import com.recomm.userservice.dto.UserResponseDTO;
import com.recomm.userservice.exception.UserAlreadyExistsException;
import com.recomm.userservice.exception.UserNotFoundException;
import com.recomm.userservice.kafka.KafkaProducer;
import com.recomm.userservice.mapper.InteractionMapper;
import com.recomm.userservice.mapper.UserMapper;
import com.recomm.userservice.model.Interaction;
import com.recomm.userservice.model.User;
import com.recomm.userservice.repository.InteractionRepository;
import com.recomm.userservice.repository.UserRepository;

import java.time.LocalDate;
import java.time.Period;
import java.util.List;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

@Service
public class UserService {
    private static final Logger logger = LoggerFactory.getLogger(UserService.class);
private final UserRepository userRepository;
private final InteractionRepository interactionRepository;
private final KafkaProducer kafkaProducer;

//Constructor
    public UserService(UserRepository userRepository, InteractionRepository interactionRepository, KafkaProducer kafkaProducer){
        this.userRepository = userRepository;
        this.kafkaProducer = kafkaProducer;
        this.interactionRepository = interactionRepository;
    }


    //get specific user by id
    public UserResponseDTO getUser(String id){
        User user = userRepository.findById(id).orElseThrow(()->new UserNotFoundException("User not found with ID: "+ id));

        return UserMapper.toResponseDTO(user);

    }

    //get if user exists
    public LoginUserResponseDTO getUserExists(String id){
        // return userRepository.existsById(id) || userRepository.existsByEmail(email);
        if (userRepository.existsById(id)){
            User user = userRepository.findById(id).orElseThrow(()->new UserNotFoundException("User not found with ID: "+ id));

            return UserMapper.toLoginResponseDto(true);
        }else{
            return UserMapper.toLoginResponseDto(false);
        }
    }

    //Create new user
    public UserResponseDTO createUser(String id, CreateUserRequestDTO userRequestDTO){

        if(userRepository.existsById(id)){
            throw new UserAlreadyExistsException("A user with this id already exists" + id);
        }

        User user = userRepository.save(UserMapper.toModel(userRequestDTO, id));

        
        //Now send pub message that user is created, for recomm service to pick up
        kafkaProducer.sendCreateEvent(user);


        return UserMapper.toResponseDTO(user);
    }

     
    public void updateProfile(String userId, UpdateUserDTO dto) {

        // if (updates.isEmpty()) {
        //     throw new IllegalArgumentException("No fields to update");
        // }

        // if (updates.size() != 1) {
        //     throw new IllegalArgumentException("Only one field can be updated at a time");
        // }

        User user = userRepository.findById(userId)
                .orElseThrow(() -> new RuntimeException("User not found"));
        
        user.setUserID(userId);
        user.setSmoker(dto.getSmoker());
        user.setDrink_Level(dto.getDrink_level());
        user.setBudget(dto.getBudget());
        user.setDress_Preference(dto.getDress_preference());
        user.setAmbience(dto.getAmbience());
        user.setTransport(dto.getTransport());
        user.setMarital_Status(dto.getMarital_status());
        user.setHijos(dto.getHijos());
        user.setPersonality(dto.getPersonality());
        user.setReligion(dto.getReligion());
        user.setInterest(dto.getInterest());
        user.setActivity(dto.getActivity());
        user.setColor(dto.getColor());
        user.setCuisine(dto.getCuisine());
        user.setHeight(dto.getHeight());
        user.setWeight(dto.getWeight());


        logger.info("User {} updated", userId);

        userRepository.save(user);

        //Now send pub message that user is edited, for recomm service to pick up
        kafkaProducer.sendUpdateEvent(user);
        
    }


    public RatePlaceDTO ratePlace(String userId, RatePlaceDTO dto){
         User user = userRepository.findById(userId)
                .orElseThrow(() -> new RuntimeException("User not found"));
        

        //store in DB
        Interaction interaction = InteractionMapper.toInteraction(dto, userId);
        interactionRepository.save(interaction);

        //For sending to recomm service
        kafkaProducer.RateEvent(user, dto.getPlaceID(), dto.getRating(), dto.getFoodRating(), dto.getServiceRating());
        

        return dto;
    }

   

    //Delete user
    public void deleteUser(String id){
        userRepository.deleteById(id);
    }


}
