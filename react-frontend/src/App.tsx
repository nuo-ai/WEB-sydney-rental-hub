import { Box, Container, Heading, Text } from '@chakra-ui/react'
import LocationAutocomplete from './components/LocationAutocomplete'

function App() {
  return (
    <Container maxW="container.md" py={10}>
      <Box>
        <Heading as="h1" size="xl" mb={2}>
          JUWO 租房
        </Heading>
        <Text fontSize="lg" mb={6}>
          在悉尼寻找您的下一个家
        </Text>
        <LocationAutocomplete />
      </Box>
    </Container>
  )
}

export default App
