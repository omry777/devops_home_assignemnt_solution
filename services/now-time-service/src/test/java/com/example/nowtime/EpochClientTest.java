package com.example.nowtime;

import org.junit.jupiter.api.Test;
import org.springframework.http.HttpMethod;
import org.springframework.http.MediaType;
import org.springframework.test.web.client.MockRestServiceServer;
import org.springframework.web.client.RestClient;

import java.time.Instant;

import static org.assertj.core.api.Assertions.assertThat;
import static org.springframework.test.web.client.ExpectedCount.once;
import static org.springframework.test.web.client.match.MockRestRequestMatchers.content;
import static org.springframework.test.web.client.match.MockRestRequestMatchers.method;
import static org.springframework.test.web.client.match.MockRestRequestMatchers.requestTo;
import static org.springframework.test.web.client.response.MockRestResponseCreators.withSuccess;

class EpochClientTest {

    @Test
    void postsInstantAndReturnsEpochFromMockedService() {
        RestClient.Builder builder = RestClient.builder().baseUrl("http://epoch-service");
        MockRestServiceServer server = MockRestServiceServer.bindTo(builder).build();
        EpochClient client = new EpochClient(builder.build());

        server.expect(once(), requestTo("http://epoch-service/epoch"))
                .andExpect(method(HttpMethod.POST))
                .andExpect(content().json("{\"date\":\"2026-06-15T10:00:00Z\"}"))
                .andRespond(withSuccess("{\"epoch\":1781517600}", MediaType.APPLICATION_JSON));

        long epoch = client.toEpoch(Instant.parse("2026-06-15T10:00:00Z"));

        assertThat(epoch).isEqualTo(1781517600L);
        server.verify();
    }
}
