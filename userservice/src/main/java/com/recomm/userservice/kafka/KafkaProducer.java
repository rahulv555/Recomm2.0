package com.recomm.userservice.kafka;

import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Service;

import com.recomm.userservice.model.User;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import user.events.CreateEvent;
import user.events.UpdateEvent;
import user.events.RateEvent;


@Service
public class KafkaProducer {

    private final KafkaTemplate<String, byte[]> kafkaTemplate;
private static final Logger log = LoggerFactory.getLogger(
      KafkaProducer.class);

    public KafkaProducer(KafkaTemplate<String, byte[]> kafkaTemplate){
        this.kafkaTemplate = kafkaTemplate;
    }


    //event sent on user creation
    public void sendCreateEvent(User user){

        //EventType to denote what type of event it is
        CreateEvent event = CreateEvent.newBuilder().setUserId(user.getUserID().toString()).setEventType("USER_CREATED").build();

        
        try{
            //sending the event to topic : "user_created"
            kafkaTemplate.send("user_created", event.toByteArray()); //this is of the form String, byte[]

        }catch(Exception e){
            log.error("Error sending User Created event: {}", event, e);
        }

    }
    


    //event sent on user update
    public void sendUpdateEvent(User user){

        //EventType to denote what type of event it is
        UpdateEvent event = UpdateEvent.newBuilder().setUserId(user.getUserID().toString()).setEventType("USER_UPDATED").build();
        
        try{
            //sending the event to topic : "user_updated"
            kafkaTemplate.send("user_updated", event.toByteArray()); //this is of the form String, byte[]

        }catch(Exception e){
            log.error("Error sending User Updated event: {}", event, e);
        }

    }


    //event sent on user creation
    public void RateEvent(User user, String placeID, Double rating, Double food_rating, Double service_rating){

        //EventType to denote what type of event it is
        RateEvent event = RateEvent.newBuilder().setUserId(user.getUserID().toString()).setPlaceId(placeID).setRating(food_rating).setFoodRating(food_rating).setServiceRating(service_rating).setEventType("USER_CREATED").build();

        
        try{
            //sending the event to topic : "rating"
            kafkaTemplate.send("rating", event.toByteArray()); //this is of the form String, byte[]

        }catch(Exception e){
            log.error("Error sending User Rated event: {}", event, e);
        }

    }

}
