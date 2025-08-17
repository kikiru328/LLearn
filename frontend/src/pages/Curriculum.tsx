// src/pages/Curriculum.tsx
import React, { useState, useEffect } from 'react';
import {
  Box,
  Button,
  VStack,
  HStack,
  Heading,
  Container,
  Text,
  Card,
  CardBody,
  Grid,
  Badge,
  IconButton,
  useToast,
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalFooter,
  ModalBody,
  ModalCloseButton,
  useDisclosure,
  Input,
  Textarea,
  Select,
  FormControl,
  FormLabel,
  Spinner,
  Alert,
  AlertIcon,
  AlertDescription,
  useColorModeValue,
  Tabs,
  TabList,
  TabPanels,
  Tab,
  TabPanel,
  Divider,
  ButtonGroup,
  Menu,
  MenuButton,
  MenuList,
  MenuItem,
} from '@chakra-ui/react';
import { AddIcon, DeleteIcon, ChevronDownIcon } from '@chakra-ui/icons';
import { useNavigate } from 'react-router-dom';
import { curriculumAPI, categoryAPI, curriculumTagAPI } from '../services/api';

interface WeekSchedule {
  week_number: number;
  title: string; 
  lessons: string[];
}

interface Curriculum {
  id: string;
  owner_id: string;
  title: string;
  visibility: 'PUBLIC' | 'PRIVATE';
  total_weeks: number;
  total_lessons: number;
  created_at: string;
  updated_at: string;
  week_schedules?: WeekSchedule[];
  category?: Category;
  tags?: Array<{ id: string; name: string; usage_count: number }>;
}

interface Category {
  id: string;
  name: string;
  color: string;
  icon?: string;
  is_active: boolean;
  usage_count: number;
}

interface CreateAICurriculumForm {
  goal: string;
  period: number;
  difficulty: 'beginner' | 'intermediate' | 'expert';
  details: string;
  category_id: string;
}

interface WeekScheduleForm {
  week_number: number;
  title: string;
  lessons: string[];
}

interface ManualCurriculumForm {
  title: string;
  visibility: 'PUBLIC' | 'PRIVATE';
  category_id: string;
  week_schedules: WeekScheduleForm[];
}

const Curriculum: React.FC = () => {
  const navigate = useNavigate();
  const [curriculums, setCurriculums] = useState<Curriculum[]>([]);
  const [loading, setLoading] = useState(true);
  const [creating, setCreating] = useState(false);
  const [error, setError] = useState('');
  
  // AI 생성 폼
  const [aiForm, setAiForm] = useState<CreateAICurriculumForm>({
    goal: '',
    period: 4,
    difficulty: 'beginner',
    details: '',
    category_id: ''
  });
  
  // 직접 생성 폼
  const [manualForm, setManualForm] = useState<ManualCurriculumForm>({
    title: '',
    visibility: 'PRIVATE',
    category_id: '',
    week_schedules: [
      {
        week_number: 1,
        title: '1주차',
        lessons: ['']
      }
    ]
  });
  
  const [categories, setCategories] = useState<Category[]>([]);
  const [loadingCategories, setLoadingCategories] = useState(false);
  
  const { isOpen: isAIModalOpen, onOpen: onAIModalOpen, onClose: onAIModalClose } = useDisclosure();
  const { isOpen: isManualModalOpen, onOpen: onManualModalOpen, onClose: onManualModalClose } = useDisclosure();
  
  const toast = useToast();

  // 다크모드 대응 색상
  const bgColor = useColorModeValue('white', 'gray.800');
  const textColor = useColorModeValue('gray.900', 'white');
  const secondaryTextColor = useColorModeValue('gray.600', 'gray.300');
  const cardBg = useColorModeValue('white', 'gray.700');
  const borderColor = useColorModeValue('gray.200', 'gray.600');

  useEffect(() => {
    fetchMyCurriculums();
    fetchCategories();
  }, []);

  const fetchCategories = async () => {
    try {
      setLoadingCategories(true);
      const response = await categoryAPI.getActive();
      setCategories(response.data || []);
    } catch (error) {
      console.error('카테고리 조회 실패:', error);
    } finally {
      setLoadingCategories(false);
    }
  };

  const fetchMyCurriculums = async () => {
    try {
      setLoading(true);
      setError('');
      const response = await curriculumAPI.getAll();
      
      let curriculumData = [];
      if (response.data && response.data.curriculums) {
        curriculumData = response.data.curriculums;
      } else if (Array.isArray(response.data)) {
        curriculumData = response.data;
      } else {
        curriculumData = [];
      }

      const curriculumsWithCategories = await loadCurriculumCategories(curriculumData);
      setCurriculums(curriculumsWithCategories);
    } catch (error: any) {
      console.error('커리큘럼 조회 실패:', error);
      setError('커리큘럼을 불러오는데 실패했습니다.');
      setCurriculums([]);
    } finally {
      setLoading(false);
    }
  };

  const loadCurriculumCategories = async (curriculums: Curriculum[]) => {
    const updatedCurriculums = await Promise.all(
      curriculums.map(async (curriculum) => {
        try {
          const response = await curriculumTagAPI.getTagsAndCategory(curriculum.id);
          return {
            ...curriculum,
            category: response.data.category,
            tags: response.data.tags
          };
        } catch (error) {
          return curriculum;
        }
      })
    );
    return updatedCurriculums;
  };

  const handleAPIError = (error: any, defaultMessage: string) => {
    let errorMessage = defaultMessage;
    
    if (error.response?.data?.detail) {
      if (Array.isArray(error.response.data.detail)) {
        errorMessage = error.response.data.detail
          .map((err: any) => err.msg || String(err))
          .join(', ');
      } else {
        errorMessage = String(error.response.data.detail);
      }
    }
    
    toast({
      title: '오류',
      description: errorMessage,
      status: 'error',
      duration: 5000,
      isClosable: true,
    });
  };

  const handleCreateAICurriculum = async () => {
    if (!aiForm.goal.trim()) {
      toast({
        title: '목표를 입력해주세요',
        status: 'warning',
        duration: 3000,
      });
      return;
    }

    try {
      setCreating(true);
      const response = await curriculumAPI.generate({
        goal: aiForm.goal,
        duration: aiForm.period,
        difficulty: aiForm.difficulty,
        details: aiForm.details
      });

      if (aiForm.category_id) {
        try {
          await curriculumTagAPI.assignCategory(response.data.id, aiForm.category_id);
        } catch (error) {
          console.warn('카테고리 할당 실패:', error);
        }
      }
      
      toast({
        title: 'AI 커리큘럼이 생성되었습니다!',
        status: 'success',
        duration: 3000,
      });
      
      setAiForm({
        goal: '',
        period: 4,
        difficulty: 'beginner',
        details: '',
        category_id: ''
      });
      onAIModalClose();
      fetchMyCurriculums();
    } catch (error: any) {
      handleAPIError(error, 'AI 커리큘럼 생성에 실패했습니다');
    } finally {
      setCreating(false);
    }
  };

  const handleCreateManualCurriculum = async () => {
    if (!manualForm.title.trim()) {
      toast({
        title: '커리큘럼 제목을 입력해주세요',
        status: 'warning',
        duration: 3000,
      });
      return;
    }

    const invalidWeeks = manualForm.week_schedules.filter(
      week => week.lessons.filter(lesson => lesson.trim()).length === 0
    );

    if (invalidWeeks.length > 0) {
      toast({
        title: '모든 주차에 최소 1개의 레슨을 입력해주세요',
        status: 'warning',
        duration: 3000,
      });
      return;
    }

    try {
      setCreating(true);
      
      const cleanedWeekSchedules = manualForm.week_schedules.map(week => ({
        ...week,
        lessons: week.lessons.filter(lesson => lesson.trim())
      }));

      const response = await curriculumAPI.createManual({
        title: manualForm.title.trim(),
        week_schedules: cleanedWeekSchedules,
        visibility: manualForm.visibility
      });

      if (manualForm.category_id) {
        try {
          await curriculumTagAPI.assignCategory(response.data.id, manualForm.category_id);
        } catch (error) {
          console.warn('카테고리 할당 실패:', error);
        }
      }
      
      toast({
        title: '커리큘럼이 생성되었습니다!',
        status: 'success',
        duration: 3000,
      });
      
      setManualForm({
        title: '',
        visibility: 'PRIVATE',
        category_id: '',
        week_schedules: [
          {
            week_number: 1,
            title: '1주차',
            lessons: ['']
          }
        ]
      });
      onManualModalClose();
      fetchMyCurriculums();
    } catch (error: any) {
      handleAPIError(error, '커리큘럼 생성에 실패했습니다');
    } finally {
      setCreating(false);
    }
  };

  // 주차 추가
  const addWeek = () => {
    const nextWeekNumber = manualForm.week_schedules.length + 1;
    if (nextWeekNumber > 24) {
      toast({
        title: '최대 24주차까지만 추가할 수 있습니다',
        status: 'warning',
        duration: 3000,
      });
      return;
    }

    setManualForm({
      ...manualForm,
      week_schedules: [
        ...manualForm.week_schedules,
        {
          week_number: nextWeekNumber,
          title: `${nextWeekNumber}주차`,
          lessons: ['']
        }
      ]
    });
  };

  // 주차 삭제
  const removeWeek = (weekIndex: number) => {
    if (manualForm.week_schedules.length <= 1) {
      toast({
        title: '최소 1개의 주차는 있어야 합니다',
        status: 'warning',
        duration: 3000,
      });
      return;
    }

    const newWeekSchedules = manualForm.week_schedules.filter((_, index) => index !== weekIndex);
    // 주차 번호 재정렬
    const reorderedWeekSchedules = newWeekSchedules.map((week, index) => ({
      ...week,
      week_number: index + 1,
      title: week.title.replace(/\d+주차/, `${index + 1}주차`)
    }));

    setManualForm({
      ...manualForm,
      week_schedules: reorderedWeekSchedules
    });
  };

  // 레슨 추가
  const addLesson = (weekIndex: number) => {
    const week = manualForm.week_schedules[weekIndex];
    if (week.lessons.length >= 5) {
      toast({
        title: '주차별 최대 5개의 레슨까지만 추가할 수 있습니다',
        status: 'warning',
        duration: 3000,
      });
      return;
    }

    const newWeekSchedules = [...manualForm.week_schedules];
    newWeekSchedules[weekIndex].lessons.push('');
    setManualForm({ ...manualForm, week_schedules: newWeekSchedules });
  };

  // 레슨 삭제
  const removeLesson = (weekIndex: number, lessonIndex: number) => {
    const week = manualForm.week_schedules[weekIndex];
    if (week.lessons.length <= 1) {
      toast({
        title: '최소 1개의 레슨은 있어야 합니다',
        status: 'warning',
        duration: 3000,
      });
      return;
    }

    const newWeekSchedules = [...manualForm.week_schedules];
    newWeekSchedules[weekIndex].lessons.splice(lessonIndex, 1);
    setManualForm({ ...manualForm, week_schedules: newWeekSchedules });
  };

  // 주차 제목 업데이트
  const updateWeekTitle = (weekIndex: number, title: string) => {
    const newWeekSchedules = [...manualForm.week_schedules];
    newWeekSchedules[weekIndex].title = title;
    setManualForm({ ...manualForm, week_schedules: newWeekSchedules });
  };

  // 레슨 업데이트
  const updateLesson = (weekIndex: number, lessonIndex: number, lesson: string) => {
    const newWeekSchedules = [...manualForm.week_schedules];
    newWeekSchedules[weekIndex].lessons[lessonIndex] = lesson;
    setManualForm({ ...manualForm, week_schedules: newWeekSchedules });
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('ko-KR', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  };

  const getVisibilityColor = (visibility: string) => {
    return visibility === 'PUBLIC' ? 'green' : 'gray';
  };

  const getVisibilityText = (visibility: string) => {
    return visibility === 'PUBLIC' ? '공개' : '비공개';
  };

  if (loading) {
    return (
      <Container maxW="6xl" py={8}>
        <VStack spacing={4}>
          <Spinner size="xl" color="blue.500" />
          <Text color={textColor}>커리큘럼을 불러오는 중...</Text>
        </VStack>
      </Container>
    );
  }

  return (
    <Container maxW="6xl" py={8}>
      <VStack spacing={6} align="stretch">
        {/* 헤더 */}
        <HStack justify="space-between" align="center">
          <Heading size="lg" color={textColor}>내 커리큘럼</Heading>
          <Menu>
            <MenuButton as={Button} leftIcon={<AddIcon />} colorScheme="blue" rightIcon={<ChevronDownIcon />}>
              새 커리큘럼 생성
            </MenuButton>
            <MenuList>
              <MenuItem onClick={onAIModalOpen}>
                🤖 AI가 생성하기
              </MenuItem>
              <MenuItem onClick={onManualModalOpen}>
                ✏️ 직접 만들기
              </MenuItem>
            </MenuList>
          </Menu>
        </HStack>

        {/* 에러 메시지 */}
        {error && (
          <Alert status="error">
            <AlertIcon />
            <AlertDescription color={textColor}>{error}</AlertDescription>
          </Alert>
        )}

        {/* 커리큘럼 목록 */}
        {curriculums.length === 0 ? (
          <Box textAlign="center" py={10} bg={cardBg} borderRadius="lg" borderWidth="1px" borderColor={borderColor}>
            <Text fontSize="lg" color={secondaryTextColor} mb={4}>
              아직 생성된 커리큘럼이 없습니다
            </Text>
            <ButtonGroup spacing={4}>
              <Button
                colorScheme="blue"
                leftIcon={<AddIcon />}
                onClick={onAIModalOpen}
              >
                AI로 생성하기
              </Button>
              <Button
                variant="outline"
                colorScheme="blue"
                leftIcon={<AddIcon />}
                onClick={onManualModalOpen}
              >
                직접 만들기
              </Button>
            </ButtonGroup>
          </Box>
        ) : (
          <Grid templateColumns="repeat(auto-fill, minmax(300px, 1fr))" gap={6}>
            {curriculums.map((curriculum) => (
              <Card 
                key={curriculum.id} 
                variant="outline" 
                bg={cardBg} 
                borderColor={borderColor}
                cursor="pointer"
                transition="all 0.2s"
                _hover={{ 
                  transform: "translateY(-2px)", 
                  shadow: "lg",
                  borderColor: "blue.300"
                }}
                onClick={() => navigate(`/curriculum/${curriculum.id}`)}
              >
                <CardBody>
                  <VStack align="stretch" spacing={3}>
                    <VStack align="stretch" spacing={2}>
                      <HStack justify="space-between" align="start">
                        <Heading size="md" noOfLines={2} color={textColor}>
                          {curriculum.title}
                        </Heading>
                        <Badge
                          colorScheme={getVisibilityColor(curriculum.visibility)}
                          variant="solid"
                        >
                          {getVisibilityText(curriculum.visibility)}
                        </Badge>
                      </HStack>

                      {curriculum.category && (
                        <HStack>
                          <Badge
                            style={{ backgroundColor: curriculum.category.color }}
                            color="white"
                            variant="solid"
                            size="sm"
                          >
                            {curriculum.category.icon && `${curriculum.category.icon} `}
                            {curriculum.category.name}
                          </Badge>
                        </HStack>
                      )}

                      {curriculum.tags && curriculum.tags.length > 0 && (
                        <HStack flexWrap="wrap" spacing={1}>
                          {curriculum.tags.slice(0, 3).map((tag) => (
                            <Badge
                              key={tag.id}
                              colorScheme="gray"
                              variant="outline"
                              size="sm"
                            >
                              #{tag.name}
                            </Badge>
                          ))}
                          {curriculum.tags.length > 3 && (
                            <Badge
                              colorScheme="gray"
                              variant="outline"
                              size="sm"
                            >
                              +{curriculum.tags.length - 3}
                            </Badge>
                          )}
                        </HStack>
                      )}
                    </VStack>

                    <HStack spacing={4} fontSize="sm" color={secondaryTextColor}>
                      <Text>{curriculum.total_weeks}주차</Text>
                      <Text>{curriculum.total_lessons}개 레슨</Text>
                    </HStack>

                    <Text fontSize="xs" color={secondaryTextColor}>
                      생성일: {formatDate(curriculum.created_at)}
                    </Text>
                  </VStack>
                </CardBody>
              </Card>
            ))}
          </Grid>
        )}

        {/* AI 커리큘럼 생성 모달 */}
        <Modal isOpen={isAIModalOpen} onClose={onAIModalClose} size="lg">
          <ModalOverlay />
          <ModalContent bg={cardBg} color={textColor}>
            <ModalHeader color={textColor}>AI 커리큘럼 생성</ModalHeader>
            <ModalCloseButton color={textColor} />
            <ModalBody>
              <VStack spacing={4}>
                <FormControl isRequired>
                  <FormLabel color={textColor}>학습 목표</FormLabel>
                  <Input
                    placeholder="예: React 웹 개발 마스터하기"
                    value={aiForm.goal}
                    onChange={(e) => setAiForm({ ...aiForm, goal: e.target.value })}
                    color={textColor}
                    borderColor={borderColor}
                  />
                </FormControl>

                <FormControl isRequired>
                  <FormLabel color={textColor}>학습 기간 (주)</FormLabel>
                  <Select
                    value={aiForm.period}
                    onChange={(e) => setAiForm({ ...aiForm, period: parseInt(e.target.value) })}
                    color={textColor}
                    borderColor={borderColor}
                  >
                    {Array.from({ length: 24 }, (_, i) => i + 1).map((week) => (
                      <option key={week} value={week} style={{ backgroundColor: cardBg, color: textColor }}>
                        {week}주
                      </option>
                    ))}
                  </Select>
                </FormControl>

                <FormControl isRequired>
                  <FormLabel color={textColor}>난이도</FormLabel>
                  <Select
                    value={aiForm.difficulty}
                    onChange={(e) => setAiForm({ ...aiForm, difficulty: e.target.value as any })}
                    color={textColor}
                    borderColor={borderColor}
                  >
                    <option value="beginner" style={{ backgroundColor: cardBg, color: textColor }}>초급</option>
                    <option value="intermediate" style={{ backgroundColor: cardBg, color: textColor }}>중급</option>
                    <option value="expert" style={{ backgroundColor: cardBg, color: textColor }}>고급</option>
                  </Select>
                </FormControl>

                <FormControl>
                  <FormLabel color={textColor}>카테고리 (선택사항)</FormLabel>
                  <Select
                    value={aiForm.category_id}
                    onChange={(e) => setAiForm({ ...aiForm, category_id: e.target.value })}
                    color={textColor}
                    borderColor={borderColor}
                    placeholder="카테고리를 선택하세요"
                  >
                    {categories.map((category) => (
                      <option key={category.id} value={category.id} style={{ backgroundColor: cardBg, color: textColor }}>
                        {category.icon && `${category.icon} `}{category.name}
                      </option>
                    ))}
                  </Select>
                </FormControl>

                <FormControl>
                  <FormLabel color={textColor}>추가 세부사항</FormLabel>
                  <Textarea
                    placeholder="특별한 요구사항이나 학습 방향을 입력해주세요"
                    value={aiForm.details}
                    onChange={(e) => setAiForm({ ...aiForm, details: e.target.value })}
                    rows={3}
                    color={textColor}
                    borderColor={borderColor}
                  />
                </FormControl>
              </VStack>
            </ModalBody>

            <ModalFooter>
              <Button variant="ghost" mr={3} onClick={onAIModalClose} color={textColor}>
                취소
              </Button>
              <Button
                colorScheme="blue"
                onClick={handleCreateAICurriculum}
                isLoading={creating}
                loadingText="생성 중..."
              >
                AI로 생성하기
              </Button>
            </ModalFooter>
          </ModalContent>
        </Modal>

        {/* 직접 커리큘럼 생성 모달 */}
        <Modal isOpen={isManualModalOpen} onClose={onManualModalClose} size="6xl">
          <ModalOverlay />
          <ModalContent bg={cardBg} color={textColor} maxH="90vh">
            <ModalHeader color={textColor}>직접 커리큘럼 만들기</ModalHeader>
            <ModalCloseButton color={textColor} />
            <ModalBody overflowY="auto">
              <VStack spacing={6} align="stretch">
                {/* 기본 정보 */}
                <Grid templateColumns={{ base: '1fr', md: '1fr 200px' }} gap={4}>
                  <FormControl isRequired>
                    <FormLabel color={textColor}>커리큘럼 제목</FormLabel>
                    <Input
                      placeholder="예: 나만의 JavaScript 학습 과정"
                      value={manualForm.title}
                      onChange={(e) => setManualForm({ ...manualForm, title: e.target.value })}
                      color={textColor}
                      borderColor={borderColor}
                    />
                  </FormControl>

                  <FormControl>
                    <FormLabel color={textColor}>공개 설정</FormLabel>
                    <Select
                      value={manualForm.visibility}
                      onChange={(e) => setManualForm({ ...manualForm, visibility: e.target.value as any })}
                      color={textColor}
                      borderColor={borderColor}
                    >
                      <option value="PRIVATE" style={{ backgroundColor: cardBg, color: textColor }}>비공개</option>
                      <option value="PUBLIC" style={{ backgroundColor: cardBg, color: textColor }}>공개</option>
                    </Select>
                  </FormControl>
                </Grid>

                <FormControl>
                  <FormLabel color={textColor}>카테고리 (선택사항)</FormLabel>
                  <Select
                    value={manualForm.category_id}
                    onChange={(e) => setManualForm({ ...manualForm, category_id: e.target.value })}
                    color={textColor}
                    borderColor={borderColor}
                    placeholder="카테고리를 선택하세요"
                  >
                    {categories.map((category) => (
                      <option key={category.id} value={category.id} style={{ backgroundColor: cardBg, color: textColor }}>
                        {category.icon && `${category.icon} `}{category.name}
                      </option>
                    ))}
                  </Select>
                </FormControl>

                <Divider />

                {/* 주차별 계획 */}
                <VStack spacing={4} align="stretch">
                  <HStack justify="space-between">
                    <Heading size="md" color={textColor}>주차별 학습 계획</Heading>
                    <Button
                      leftIcon={<AddIcon />}
                      size="sm"
                      colorScheme="green"
                      onClick={addWeek}
                      isDisabled={manualForm.week_schedules.length >= 24}
                    >
                      주차 추가
                    </Button>
                  </HStack>

                  {manualForm.week_schedules.map((week, weekIndex) => (
                    <Card key={weekIndex} variant="outline" borderColor={borderColor}>
                      <CardBody>
                        <VStack spacing={4} align="stretch">
                          <HStack justify="space-between">
                            <FormControl>
                              <FormLabel color={textColor} fontSize="sm">
                                {week.week_number}주차 제목
                              </FormLabel>
                              <Input
                                value={week.title}
                                onChange={(e) => updateWeekTitle(weekIndex, e.target.value)}
                                placeholder={`${week.week_number}주차`}
                                color={textColor}
                                borderColor={borderColor}
                                size="sm"
                              />
                            </FormControl>
                            
                            {manualForm.week_schedules.length > 1 && (
                              <IconButton
                                aria-label="주차 삭제"
                                icon={<DeleteIcon />}
                                size="sm"
                                colorScheme="red"
                                variant="ghost"
                                onClick={() => removeWeek(weekIndex)}
                                alignSelf="flex-end"
                              />
                            )}
                          </HStack>

                          <VStack spacing={2} align="stretch">
                            <HStack justify="space-between">
                              <Text fontSize="sm" fontWeight="semibold" color={textColor}>
                                레슨 목록
                              </Text>
                              <Button
                                leftIcon={<AddIcon />}
                                size="xs"
                                variant="ghost"
                                colorScheme="blue"
                                onClick={() => addLesson(weekIndex)}
                                isDisabled={week.lessons.length >= 5}
                              >
                                레슨 추가
                              </Button>
                            </HStack>

                            {week.lessons.map((lesson, lessonIndex) => (
                              <HStack key={lessonIndex} spacing={2}>
                                <Text fontSize="sm" color={secondaryTextColor} minW="20px">
                                  {lessonIndex + 1}.
                                </Text>
                                <Input
                                  value={lesson}
                                  onChange={(e) => updateLesson(weekIndex, lessonIndex, e.target.value)}
                                  placeholder={`레슨 ${lessonIndex + 1} 내용`}
                                  color={textColor}
                                  borderColor={borderColor}
                                  size="sm"
                                />
                                {week.lessons.length > 1 && (
                                  <IconButton
                                    aria-label="레슨 삭제"
                                    icon={<DeleteIcon />}
                                    size="xs"
                                    colorScheme="red"
                                    variant="ghost"
                                    onClick={() => removeLesson(weekIndex, lessonIndex)}
                                  />
                                )}
                              </HStack>
                            ))}
                          </VStack>
                        </VStack>
                      </CardBody>
                    </Card>
                  ))}
                </VStack>
              </VStack>
            </ModalBody>

            <ModalFooter>
              <Button variant="ghost" mr={3} onClick={onManualModalClose} color={textColor}>
                취소
              </Button>
              <Button
                colorScheme="blue"
                onClick={handleCreateManualCurriculum}
                isLoading={creating}
                loadingText="생성 중..."
              >
                커리큘럼 생성
              </Button>
            </ModalFooter>
          </ModalContent>
        </Modal>
      </VStack>
    </Container>
  );
};

export default Curriculum;
