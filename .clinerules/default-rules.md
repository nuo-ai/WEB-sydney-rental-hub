# 用中文沟通

# Sydney Rental Hub - Project Intelligence

## Project Context
This is a Chinese student-focused rental platform for Sydney, emphasizing commute time to universities as the primary search criterion. The project uses a "UI-first" development approach with FastAPI backend and vanilla HTML/CSS/JS frontend.

## Key Patterns Discovered

### Development Workflow
- **UI-First Strategy**: Build complete static UI before backend integration
- **Chinese-First Content**: All documentation and user-facing content in Chinese
- **Memory Bank Driven**: Project relies heavily on structured documentation for context
- **MVP Focus**: Prioritize core commute-time sorting feature over advanced features

### Technical Preferences
- **Vanilla Frontend**: Prefer native HTML/CSS/JS over frameworks for simplicity
- **GraphQL over REST**: Chosen for flexible data querying and type safety
- **PostgreSQL + PostGIS**: Essential for geospatial calculations
- **Cloud-Native Deployment**: Separate hosting for frontend (Netlify) and backend (Render/Railway)

### User Experience Priorities
1. **Commute Time as Primary Filter**: Users search by university, results sorted by travel time
2. **Mobile-First Design**: Target audience primarily uses mobile devices
3. **Chinese Language Support**: All UI and content in Chinese
4. **Trust and Transparency**: Clear pricing, professional consultation services

### Code Organization
- **Memory Bank Structure**: Maintain 6 core documentation files
- **Separation of Concerns**: Clear frontend/backend boundaries
- **Progressive Enhancement**: Start with static UI, add interactivity incrementally

## Critical Implementation Paths

### Authentication Flow
1. Static UI pages first (login.html, register.html, profile.html)
2. Backend JWT implementation
3. Frontend-backend integration
4. State management with localStorage

### Property Search Flow
1. University selection as primary filter
2. Geospatial distance calculation
3. Transit time estimation
4. Results sorting and display

### Data Architecture
- **Property Data**: Location, price, features
- **Transit Data**: Stations, routes, timing
- **University Data**: Campus locations, popular destinations
- **User Data**: Preferences, saved properties, search history

## Known Challenges

### Technical Challenges
- **Geospatial Queries**: Complex distance and transit time calculations
- **Real-time Data**: Transit schedules and property availability
- **Mobile Performance**: Optimizing map and search performance on mobile

### Business Challenges
- **Data Sources**: Accessing reliable Australian property and transit data
- **Market Competition**: Differentiating from established platforms
- **Trust Building**: Establishing credibility with international students

## Development Environment
- **IDE**: Visual Studio Code
- **Backend Server**: `uvicorn server.main:app --reload`
- **Frontend Server**: `netlify dev`
- **Database**: PostgreSQL with PostGIS extension
- **Version Control**: Git + GitHub

## Quality Standards
- **Documentation**: Every major change updates Memory Bank
- **Mobile Testing**: All features tested on mobile devices
- **Chinese Localization**: All user-facing text in Chinese
- **Performance**: Sub-3-second search results
- **Security**: JWT tokens, HTTPS, input validation

## Future Considerations
- **WeChat Mini-Program**: Long-term expansion goal
- **Native Mobile Apps**: iOS/Android development
- **Microservices**: Potential backend service separation
- **Real-time Features**: Live chat, notifications
- **Payment Integration**: Stripe for consultation services

## User Workflow Insights
- **Primary Use Case**: Pre-arrival students searching from China
- **Decision Factors**: Commute time > Price > Amenities
- **Trust Signals**: Professional consultation, transparent pricing
- **Mobile Usage**: Expect thumb-friendly navigation and quick loading

## Success Metrics
- **User Engagement**: Time spent on property details
- **Conversion**: Saved properties to consultation purchases
- **Performance**: Search response time under 3 seconds
- **Mobile Experience**: >90% mobile traffic accommodation

This project intelligence will evolve as development progresses and user feedback is gathered.